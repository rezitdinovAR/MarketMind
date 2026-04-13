"""Comparator — compares product groups using LLM + rule-based scoring."""

from __future__ import annotations

import logging
from pathlib import Path

from marketmind.llm_client import LLMClient
from marketmind.models import ProductAnalysis, QuerySpec, WorkflowStage

logger = logging.getLogger("marketmind")


FALLBACK_SYSTEM_PROMPT = (
    "Сравни товары и оцени value_score и fit_score (0-1). "
    "Верни JSON с массивом products и comparison_summary."
)


def _load_prompt(prompts_dir: Path) -> str:
    path = prompts_dir / "comparison.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return FALLBACK_SYSTEM_PROMPT


def _build_comparison_input(analyzed: list[ProductAnalysis], query_spec: QuerySpec) -> str:
    lines = [
        f"Запрос пользователя: {query_spec.raw_query}",
        f"Категория: {query_spec.category or 'не определена'}",
        f"Бюджет: {query_spec.budget_min or '?'} — {query_spec.budget_max or '?'} руб.",
        f"Обязательные характеристики: {', '.join(query_spec.must_have) or 'не указаны'}",
        f"Желательные характеристики: {', '.join(query_spec.nice_to_have) or 'не указаны'}",
        "",
        "--- Товары для сравнения (сгруппированы по модели) ---",
    ]

    for a in analyzed:
        g = a.product_group
        rs = a.review_summary

        lines.append(f"\nID: {g.group_id}")
        lines.append(f"Модель: {g.canonical_name}")
        lines.append(f"Лучшая цена: {g.best_price} руб. ({g.best_marketplace})")

        # Price across marketplaces
        prices = [f"{o.marketplace}: {o.price} руб." for o in g.offers]
        lines.append(f"Цены: {' | '.join(prices)}")

        lines.append(f"Средний рейтинг: {g.avg_rating}/5 ({g.total_review_count} отзывов со всех площадок)")
        if rs.pros:
            lines.append(f"Плюсы: {'; '.join(rs.pros)}")
        if rs.cons:
            lines.append(f"Минусы: {'; '.join(rs.cons)}")
        lines.append(f"Резюме: {rs.summary}")
        lines.append(f"Доверие к отзывам: {rs.trust_score}")
        if hasattr(g, 'attributes') and g.attributes:
            attrs_str = ", ".join(f"{k}: {v}" for k, v in g.attributes.items())
            lines.append(f"Характеристики: {attrs_str}")

    return "\n".join(lines)


def run_comparator(state: dict, llm: LLMClient, prompts_dir: Path, model_override: str | None = None) -> dict:
    """LangGraph node: compare analyzed product groups."""
    analyzed: list[ProductAnalysis] = state.get("analyzed_products", [])
    query_spec: QuerySpec = state.get("query_spec")

    if not analyzed or not query_spec:
        return {
            "analyzed_products": analyzed,
            "stage": WorkflowStage.COMPARED,
            "errors": ["No products to compare"],
        }

    system_prompt = _load_prompt(prompts_dir)
    user_input = _build_comparison_input(analyzed, query_spec)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    try:
        result = llm.call_json(messages, temperature=0.3, max_tokens=2048, model_override=model_override)
        llm_products = {p["product_id"]: p for p in result.get("products", [])}

        for a in analyzed:
            if a.product_group.group_id in llm_products:
                scores = llm_products[a.product_group.group_id]
                a.value_score = min(1.0, max(0.0, scores.get("value_score", 0.5)))
                a.fit_score = min(1.0, max(0.0, scores.get("fit_score", 0.5)))

        # Rule-based adjustments
        for a in analyzed:
            if query_spec.budget_max and a.product_group.best_price > query_spec.budget_max:
                a.fit_score = min(a.fit_score, 0.3)
            # Boost products with significant discounts
            for offer in a.product_group.offers:
                if offer.original_price and offer.price < offer.original_price:
                    discount = 1 - (offer.price / offer.original_price)
                    a.value_score = min(1.0, a.value_score + discount * 0.1)
                    break  # one boost per group is enough

        logger.info(f"Compared {len(analyzed)} product groups", extra={"stage": "comparator"})

    except Exception as e:
        logger.warning(f"LLM comparison failed, using heuristic: {e}")
        max_price = max(a.product_group.best_price for a in analyzed) if analyzed else 1
        for a in analyzed:
            a.value_score = round(
                1 - (a.product_group.best_price / max_price) * 0.5 + a.product_group.avg_rating / 10, 2
            )
            a.value_score = min(1.0, max(0.0, a.value_score))
            a.fit_score = round(a.product_group.avg_rating / 5, 2)
            if query_spec.budget_max and a.product_group.best_price > query_spec.budget_max:
                a.fit_score = 0.2

    stats = llm.get_usage_stats()
    return {
        "analyzed_products": analyzed,
        "stage": WorkflowStage.COMPARED,
        "llm_calls": stats["calls"],
        "total_tokens": stats["total_tokens"],
        "total_cost": stats["total_cost"],
    }
