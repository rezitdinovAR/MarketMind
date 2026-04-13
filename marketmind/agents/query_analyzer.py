"""QueryAnalyzer — parses user query into structured QuerySpec."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from marketmind.llm_client import LLMClient
from marketmind.models import AgentState, QuerySpec, WorkflowStage

logger = logging.getLogger("marketmind")


FALLBACK_SYSTEM_PROMPT = (
    "Ты — AI-ассистент для анализа запросов покупателей. "
    "Извлеки из запроса: category, budget_min, budget_max, must_have, nice_to_have, "
    "needs_clarification, clarification_questions. Отвечай ТОЛЬКО валидным JSON."
)

# Regex patterns that indicate prompt injection attempts
_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"ignore\s+(all\s+)?above", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?previous", re.IGNORECASE),
    re.compile(r"forget\s+(all\s+)?previous", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\b", re.IGNORECASE),
    re.compile(r"new\s+system\s+prompt", re.IGNORECASE),
    re.compile(r"^system\s*:", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\bsystem\s*prompt\b", re.IGNORECASE),
    re.compile(r"act\s+as\s+(if\s+)?(you\s+are|a)\b", re.IGNORECASE),
    re.compile(r"pretend\s+(you\s+are|to\s+be)\b", re.IGNORECASE),
    re.compile(r"override\s+(your\s+)?instructions", re.IGNORECASE),
    re.compile(r"<\s*/?\s*system\s*>", re.IGNORECASE),
    # Russian variants
    re.compile(r"игнорируй\s+(все\s+)?предыдущие", re.IGNORECASE),
    re.compile(r"забудь\s+(все\s+)?инструкции", re.IGNORECASE),
    re.compile(r"ты\s+теперь\b", re.IGNORECASE),
    re.compile(r"новая\s+роль", re.IGNORECASE),
]


def _detect_injection(query: str) -> bool:
    """Check if the query contains prompt injection patterns."""
    for pattern in _INJECTION_PATTERNS:
        if pattern.search(query):
            return True
    return False


def _load_prompt(prompts_dir: Path) -> str:
    path = prompts_dir / "query_analysis.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return FALLBACK_SYSTEM_PROMPT


def _sanitize_input(query: str) -> str:
    """Input sanitization with prompt injection detection."""
    if len(query) > 1000:
        query = query[:1000]
    query = query.strip()

    if _detect_injection(query):
        logger.warning(f"Prompt injection detected in query: {query[:100]!r}")
        raise PromptInjectionError("Обнаружена попытка манипуляции. Пожалуйста, введите обычный запрос о товаре.")

    return query


class PromptInjectionError(Exception):
    """Raised when prompt injection is detected in user input."""
    pass


def _build_messages(system_prompt: str, user_query: str, chat_history: list[dict]) -> list[dict]:
    """Build LLM messages with conversation history for multi-turn clarification.

    If there's chat history, the LLM sees the full dialogue so it can synthesize
    a complete product query from incremental user answers.
    """
    messages = [{"role": "system", "content": system_prompt}]

    if chat_history:
        # Feed the full conversation so the LLM has context from prior turns.
        # Filter to user/assistant roles only (skip system).
        for msg in chat_history:
            if msg.get("role") in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})
        # The current message is already the last item in chat_history,
        # but if it's not, append it explicitly.
        if not chat_history or chat_history[-1].get("content") != user_query:
            messages.append({"role": "user", "content": user_query})
    else:
        messages.append({"role": "user", "content": user_query})

    return messages


def run_query_analyzer(state: dict, llm: LLMClient, prompts_dir: Path, model_override: str | None = None) -> dict:
    """LangGraph node: parse user query into QuerySpec."""
    user_query = state.get("user_query", "")
    chat_history: list[dict] = state.get("chat_history", [])

    try:
        user_query = _sanitize_input(user_query)
    except PromptInjectionError as e:
        logger.warning(f"Prompt injection blocked: {user_query[:100]!r}")
        return {
            "query_spec": QuerySpec(
                raw_query=user_query,
                needs_clarification=True,
                clarification_questions=[str(e)],
            ),
            "stage": WorkflowStage.QUERY_PARSED,
            "errors": ["Prompt injection detected"],
        }

    if len(user_query) < 2:
        return {
            "query_spec": QuerySpec(
                raw_query=user_query,
                needs_clarification=True,
                clarification_questions=["Пожалуйста, опишите подробнее, какой товар вы ищете."],
            ),
            "stage": WorkflowStage.QUERY_PARSED,
        }

    system_prompt = _load_prompt(prompts_dir)
    messages = _build_messages(system_prompt, user_query, chat_history)

    try:
        result = llm.call_json(messages, temperature=0.2, max_tokens=1024, model_override=model_override)

        query_spec = QuerySpec(
            raw_query=user_query,
            category=result.get("category"),
            budget_min=result.get("budget_min"),
            budget_max=result.get("budget_max"),
            must_have=result.get("must_have", []),
            nice_to_have=result.get("nice_to_have", []),
            marketplace_priority=result.get("marketplace_priority", ["ozon", "wildberries", "yandex"]),
            needs_clarification=result.get("needs_clarification", False),
            clarification_questions=result.get("clarification_questions", []),
        )

        logger.info(
            f"Query parsed: category={query_spec.category}, budget_max={query_spec.budget_max}",
            extra={"stage": "query_analyzer"},
        )

        stats = llm.get_usage_stats()
        return {
            "query_spec": query_spec,
            "stage": WorkflowStage.QUERY_PARSED,
            "llm_calls": stats["calls"],
            "total_tokens": stats["total_tokens"],
            "total_cost": stats["total_cost"],
        }

    except Exception as e:
        logger.error(f"Query analysis failed: {e}", extra={"stage": "query_analyzer"})
        return {
            "query_spec": QuerySpec(
                raw_query=user_query,
                needs_clarification=True,
                clarification_questions=["Не удалось обработать запрос. Попробуйте переформулировать."],
            ),
            "stage": WorkflowStage.QUERY_PARSED,
            "errors": [f"QueryAnalyzer error: {e}"],
        }
