"""LangGraph Orchestrator — main pipeline for MarketMind."""

from __future__ import annotations

import logging
import re
import time
from functools import partial
from pathlib import Path
from typing import Any, TypedDict, Optional

from langgraph.graph import END, StateGraph

from marketmind.agents.comparator import run_comparator
from marketmind.agents.product_searcher import run_product_searcher
from marketmind.agents.query_analyzer import run_query_analyzer
from marketmind.agents.recommender import run_recommender
from marketmind.agents.review_analyzer import run_review_analyzer
from marketmind.config import LLMConfig, Settings
from marketmind.llm_client import LLMClient
from marketmind.models import (
    ProductAnalysis,
    ProductGroup,
    QuerySpec,
    Recommendation,
    Review,
    WorkflowStage,
)
from marketmind.observability import RequestTrace
from marketmind.tools.mock_provider import MockDataProvider

logger = logging.getLogger("marketmind")


# --- LangGraph State (TypedDict for LangGraph compatibility) ---

class GraphState(TypedDict, total=False):
    user_query: str
    chat_history: list[dict]  # full conversation for multi-turn clarification
    query_spec: Optional[QuerySpec]
    product_groups: list[ProductGroup]
    group_reviews: dict[str, list[Review]]
    analyzed_products: list[ProductAnalysis]
    recommendation: Optional[Recommendation]
    stage: WorkflowStage
    errors: list[str]
    llm_calls: int
    total_tokens: int
    total_cost: float


# --- Intent guard (product-related query filter) ---

# Keywords that indicate a product search intent (Russian + English)
_PRODUCT_KEYWORDS = re.compile(
    r"(купить|найти|подобрать|выбрать|посоветуй|порекомендуй|сравни|ищу|нужен|нужна|нужно|нужны|"
    r"хочу|хотел|подскажи|покажи|товар|продукт|модель|бренд|марка|цена|бюджет|дешев|дорог|"
    r"рейтинг|отзыв|обзор|характеристик|наушник|ноутбук|телефон|смартфон|планшет|телевизор|"
    r"пылесос|холодильник|стиральн|микроволн|кофемашин|чайник|утюг|фен|камер|"
    r"buy|find|search|compare|recommend|product|price|budget|review|headphone|laptop|phone)",
    re.IGNORECASE,
)

# Keywords that indicate clearly off-topic queries
_OFFTOPIC_PATTERNS = [
    re.compile(r"(напиши|сочини|расскажи)\s+(стих|сказк|историю|рассказ|эссе|код|программу)", re.IGNORECASE),
    re.compile(r"(кто\s+ты|что\s+ты\s+умеешь|как\s+тебя\s+зовут)", re.IGNORECASE),
    re.compile(r"(реши|вычисли|посчитай)\s+(задач|уравнен|пример|интеграл)", re.IGNORECASE),
    re.compile(r"(переведи|translate)\b", re.IGNORECASE),
]


def _node_intent_guard(state: GraphState) -> GraphState:
    """Guard node: check if the query is product-related."""
    user_query = state.get("user_query", "")
    chat_history = state.get("chat_history", [])

    # If there's active clarification dialog, let it through (continuation of product search)
    if len(chat_history) > 1:
        return {"stage": WorkflowStage.INIT}

    # Check for off-topic patterns first
    for pattern in _OFFTOPIC_PATTERNS:
        if pattern.search(user_query):
            logger.info(f"Intent guard: off-topic query detected: {user_query[:80]!r}")
            return {
                "query_spec": QuerySpec(
                    raw_query=user_query,
                    needs_clarification=True,
                    clarification_questions=[
                        "Я — ассистент по подбору товаров на маркетплейсах. "
                        "Пожалуйста, опишите, какой товар вы ищете."
                    ],
                ),
                "stage": WorkflowStage.QUERY_PARSED,
            }

    # If query is very short and has no product keywords, flag it
    if len(user_query) < 5 and not _PRODUCT_KEYWORDS.search(user_query):
        return {"stage": WorkflowStage.INIT}  # pass through to parse_query, it handles short queries

    # No product keywords at all in a long query — likely off-topic
    if len(user_query) > 20 and not _PRODUCT_KEYWORDS.search(user_query):
        logger.info(f"Intent guard: no product keywords in query: {user_query[:80]!r}")
        return {
            "query_spec": QuerySpec(
                raw_query=user_query,
                needs_clarification=True,
                clarification_questions=[
                    "Я — ассистент по подбору товаров. Ваш запрос не похож на поиск товара. "
                    "Опишите, какой товар вы хотите найти, и я помогу подобрать лучший вариант."
                ],
            ),
            "stage": WorkflowStage.QUERY_PARSED,
        }

    return {"stage": WorkflowStage.INIT}


def _route_after_guard(state: GraphState) -> str:
    """Route after intent guard: proceed to parse or end with clarification."""
    query_spec = state.get("query_spec")
    if query_spec and query_spec.needs_clarification:
        return "end_clarification"
    return "parse_query"


# --- Routing functions ---

def _route_after_parse(state: GraphState) -> str:
    """Route after query parsing: clarify or search."""
    query_spec = state.get("query_spec")
    if not query_spec:
        return "end_no_results"
    if query_spec.needs_clarification:
        return "end_clarification"
    return "search_products"


def _route_after_search(state: GraphState) -> str:
    """Route after search: analyze or no results."""
    groups = state.get("product_groups", [])
    if not groups:
        return "end_no_results"
    return "analyze_reviews"


# --- Node wrappers ---

def _node_parse_query(state: GraphState, llm: LLMClient, prompts_dir: Path, llm_config: LLMConfig) -> GraphState:
    trace_start = time.time()
    model = llm_config.get_model_for_stage("query_analysis")
    model_override = model if model != llm_config.model else None

    for attempt in range(2):
        try:
            result = run_query_analyzer(state, llm, prompts_dir, model_override=model_override)
            logger.info(f"parse_query took {time.time() - trace_start:.2f}s (model={model})")
            return result
        except Exception as e:
            logger.warning(f"parse_query attempt {attempt + 1} failed: {e}")
            if attempt == 0:
                continue
            # Final failure: return clarification request
            return {
                "query_spec": QuerySpec(
                    raw_query=state.get("user_query", ""),
                    needs_clarification=True,
                    clarification_questions=["Не удалось обработать запрос. Попробуйте переформулировать."],
                ),
                "stage": WorkflowStage.QUERY_PARSED,
                "errors": [f"QueryAnalyzer error: {e}"],
            }


def _node_search_products(
    state: GraphState,
    mock_provider: MockDataProvider,
    enabled_sources: dict[str, bool],
    max_results_total: int,
    min_rating: float,
    max_reviews_per_product: int = 15,
) -> GraphState:
    trace_start = time.time()
    try:
        result = run_product_searcher(state, mock_provider, enabled_sources, max_results_total, min_rating, max_reviews_per_product)
        logger.info(f"search_products took {time.time() - trace_start:.2f}s")
        return result
    except Exception as e:
        logger.error(f"search_products failed: {e}")
        return {
            "product_groups": [],
            "group_reviews": {},
            "stage": WorkflowStage.PRODUCTS_FOUND,
            "errors": [f"Search error: {e}"],
        }


def _node_analyze_reviews(state: GraphState, llm: LLMClient, prompts_dir: Path, llm_config: LLMConfig) -> GraphState:
    trace_start = time.time()
    model = llm_config.get_model_for_stage("review_analysis")
    try:
        result = run_review_analyzer(state, llm, prompts_dir, model_override=model if model != llm_config.model else None)
        logger.info(f"analyze_reviews took {time.time() - trace_start:.2f}s (model={model})")
        return result
    except Exception as e:
        logger.error(f"analyze_reviews failed, using partial data: {e}")
        return {
            "analyzed_products": state.get("analyzed_products", []),
            "stage": WorkflowStage.REVIEWS_ANALYZED,
            "errors": [f"ReviewAnalyzer error (partial results): {e}"],
        }


def _node_compare(state: GraphState, llm: LLMClient, prompts_dir: Path, llm_config: LLMConfig) -> GraphState:
    trace_start = time.time()
    model = llm_config.get_model_for_stage("comparison")
    try:
        result = run_comparator(state, llm, prompts_dir, model_override=model if model != llm_config.model else None)
        logger.info(f"compare_products took {time.time() - trace_start:.2f}s (model={model})")
        return result
    except Exception as e:
        logger.error(f"compare_products failed, passing through: {e}")
        return {
            "analyzed_products": state.get("analyzed_products", []),
            "stage": WorkflowStage.COMPARED,
            "errors": [f"Comparator error: {e}"],
        }


def _node_recommend(state: GraphState, llm: LLMClient, prompts_dir: Path, llm_config: LLMConfig) -> GraphState:
    trace_start = time.time()
    model = llm_config.get_model_for_stage("recommendation")
    try:
        result = run_recommender(state, llm, prompts_dir, model_override=model if model != llm_config.model else None)
        logger.info(f"generate_recommendation took {time.time() - trace_start:.2f}s (model={model})")
        return result
    except Exception as e:
        logger.error(f"generate_recommendation failed: {e}")
        return {
            "recommendation": Recommendation(
                explanation="Не удалось сформировать детальную рекомендацию.",
                confidence=0.0,
                user_query=state.get("user_query", ""),
            ),
            "stage": WorkflowStage.RECOMMENDED,
            "errors": [f"Recommender error: {e}"],
        }


# --- User-facing error messages ---

_USER_MESSAGES = {
    "llm_unavailable": "Сервис временно перегружен. Попробуйте позже.",
    "no_results": "К сожалению, по вашему запросу ничего не найдено. Попробуйте расширить критерии.",
    "partial_results": "Найдено меньше товаров, чем обычно. Показываем лучшие из доступных.",
    "timeout": "Поиск занял слишком много времени. Показываем частичные результаты.",
}


def get_user_message(state: GraphState) -> str | None:
    """Generate user-facing message based on final pipeline state."""
    errors = state.get("errors", [])

    # Check for LLM budget/timeout errors
    for err in errors:
        if "BudgetExceeded" in err or "Max duration" in err:
            if state.get("recommendation"):
                return _USER_MESSAGES["timeout"]
            return _USER_MESSAGES["llm_unavailable"]

    # No products found
    if not state.get("product_groups"):
        return _USER_MESSAGES["no_results"]

    # Partial results (fewer than expected)
    groups = state.get("product_groups", [])
    if 0 < len(groups) < 3 and state.get("recommendation"):
        return _USER_MESSAGES["partial_results"]

    return None


# --- Build graph ---

def build_graph(settings: Settings, llm: LLMClient) -> StateGraph:
    """Build the LangGraph agent pipeline."""
    prompts_dir = settings.get_prompts_path()
    mock_provider = MockDataProvider(settings.get_mock_data_path())

    # Determine enabled sources
    enabled_sources = {
        name: src.enabled
        for name, src in settings.search.sources.items()
    }

    graph = StateGraph(GraphState)

    # Add nodes with dependencies injected via partial
    llm_config = settings.llm

    graph.add_node("intent_guard", _node_intent_guard)
    graph.add_node(
        "parse_query",
        partial(_node_parse_query, llm=llm, prompts_dir=prompts_dir, llm_config=llm_config),
    )
    graph.add_node(
        "search_products",
        partial(
            _node_search_products,
            mock_provider=mock_provider,
            enabled_sources=enabled_sources,
            max_results_total=settings.search.max_results_total,
            min_rating=settings.search.min_rating,
            max_reviews_per_product=settings.analysis.max_reviews_per_product,
        ),
    )
    graph.add_node(
        "analyze_reviews",
        partial(_node_analyze_reviews, llm=llm, prompts_dir=prompts_dir, llm_config=llm_config),
    )
    graph.add_node(
        "compare_products",
        partial(_node_compare, llm=llm, prompts_dir=prompts_dir, llm_config=llm_config),
    )
    graph.add_node(
        "generate_recommendation",
        partial(_node_recommend, llm=llm, prompts_dir=prompts_dir, llm_config=llm_config),
    )

    # Set entry point — intent guard runs before query parsing
    graph.set_entry_point("intent_guard")

    # Intent guard → parse_query or end
    graph.add_conditional_edges(
        "intent_guard",
        _route_after_guard,
        {
            "parse_query": "parse_query",
            "end_clarification": END,
        },
    )

    # Conditional edges
    graph.add_conditional_edges(
        "parse_query",
        _route_after_parse,
        {
            "search_products": "search_products",
            "end_clarification": END,
            "end_no_results": END,
        },
    )
    graph.add_conditional_edges(
        "search_products",
        _route_after_search,
        {
            "analyze_reviews": "analyze_reviews",
            "end_no_results": END,
        },
    )

    # Linear edges
    graph.add_edge("analyze_reviews", "compare_products")
    graph.add_edge("compare_products", "generate_recommendation")
    graph.add_edge("generate_recommendation", END)

    return graph


class Orchestrator:
    """Main orchestrator for MarketMind pipeline."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = LLMClient(settings.llm)
        self._graph = build_graph(settings, self.llm)
        self._compiled = self._graph.compile()

    def get_graph(self) -> StateGraph:
        """Return the compiled graph for visualization or inspection."""
        return self._graph

    def run_with_config(self, user_query: str, config_overrides: dict | None = None) -> "Recommendation":
        """Run pipeline with custom config overrides.

        Args:
            user_query: The user query.
            config_overrides: Dict of setting overrides (e.g. {"llm": {"model": "deepseek-reasoner"}}).
        """
        if not config_overrides:
            result = self.run(user_query)
            return result.get("recommendation")

        # Apply overrides to a copy of settings
        import copy
        settings_data = copy.deepcopy(self.settings.model_dump())
        for section, values in config_overrides.items():
            if section in settings_data and isinstance(values, dict):
                settings_data[section].update(values)

        from marketmind.config import Settings
        temp_settings = Settings(**settings_data)
        temp_llm = LLMClient(temp_settings.llm)
        temp_graph = build_graph(temp_settings, temp_llm)
        temp_compiled = temp_graph.compile()

        temp_llm.reset_session()
        initial_state: GraphState = {
            "user_query": user_query,
            "chat_history": [],
            "query_spec": None,
            "product_groups": [],
            "group_reviews": {},
            "analyzed_products": [],
            "recommendation": None,
            "stage": WorkflowStage.INIT,
            "errors": [],
            "llm_calls": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
        }

        result = temp_compiled.invoke(initial_state)
        return result.get("recommendation")

    def run(self, user_query: str, chat_history: list[dict] | None = None) -> GraphState:
        """Run the full pipeline and return final state.

        Args:
            user_query: The latest user message.
            chat_history: Full conversation history (list of {"role": ..., "content": ...}).
                          Used to preserve context during multi-turn clarification.
        """
        self.llm.reset_session()

        initial_state: GraphState = {
            "user_query": user_query,
            "chat_history": chat_history or [],
            "query_spec": None,
            "product_groups": [],
            "group_reviews": {},
            "analyzed_products": [],
            "recommendation": None,
            "stage": WorkflowStage.INIT,
            "errors": [],
            "llm_calls": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
        }

        trace = RequestTrace()
        logger.info(
            f"Starting pipeline for query: {user_query!r}",
            extra={"request_id": trace.request_id},
        )

        try:
            final_state = self._compiled.invoke(initial_state)
            trace.finish("success")
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            trace.finish("error", str(e))
            final_state = {**initial_state, "errors": [str(e)], "stage": WorkflowStage.ERROR}

        # Save eval checkpoints in debug mode
        if self.settings.app.debug:
            from marketmind.observability import save_eval_checkpoint
            logs_path = self.settings.get_logs_path()
            rid = trace.request_id

            if final_state.get("query_spec"):
                save_eval_checkpoint(logs_path, rid, "query_parse",
                    {"user_query": user_query},
                    {"query_spec": str(final_state["query_spec"])})
            if final_state.get("recommendation"):
                save_eval_checkpoint(logs_path, rid, "recommendation",
                    {"user_query": user_query, "product_count": len(final_state.get("product_groups", []))},
                    {"recommendation": str(final_state["recommendation"])})

        # Update trace with final stats
        stats = self.llm.get_usage_stats()
        trace.total_llm_calls = stats["calls"]
        trace.total_tokens = stats["total_tokens"]
        trace.total_cost = stats["total_cost"]

        logger.info(
            f"Pipeline finished: status={trace.final_status}, "
            f"llm_calls={stats['calls']}, tokens={stats['total_tokens']}, "
            f"cost=${stats['total_cost']:.4f}, duration={trace.duration_seconds:.1f}s",
            extra={"request_id": trace.request_id},
        )

        # Save trace
        try:
            trace.save(self.settings.get_logs_path())
        except Exception:
            pass

        return final_state

    def stream(self, user_query: str):
        """Stream pipeline execution, yielding state after each node."""
        self.llm.reset_session()

        initial_state: GraphState = {
            "user_query": user_query,
            "chat_history": [],
            "query_spec": None,
            "product_groups": [],
            "group_reviews": {},
            "analyzed_products": [],
            "recommendation": None,
            "stage": WorkflowStage.INIT,
            "errors": [],
            "llm_calls": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
        }

        for event in self._compiled.stream(initial_state):
            yield event
