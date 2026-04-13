"""ReviewAnalyzer — summarizes aggregated product reviews using LLM."""

from __future__ import annotations

import logging
from pathlib import Path

from marketmind.llm_client import LLMClient
from marketmind.models import (
    ProductAnalysis,
    ProductGroup,
    Review,
    ReviewSummary,
    WorkflowStage,
)

logger = logging.getLogger("marketmind")


FALLBACK_SYSTEM_PROMPT = (
    "Проанализируй отзывы и верни JSON: "
    '{"pros": [...], "cons": [...], "summary": "...", "trust_score": 0.0-1.0}. '
    "Отвечай ТОЛЬКО валидным JSON."
)


def _load_prompt(prompts_dir: Path) -> str:
    path = prompts_dir / "review_analysis.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return FALLBACK_SYSTEM_PROMPT


def _format_reviews(reviews: list[Review]) -> str:
    lines = []
    for r in reviews:
        stars = "*" * r.rating
        verified = " [Verified]" if r.verified_purchase else ""
        lines.append(f"[{stars}]{verified} ({r.date}): {r.text}")
    return "\n\n".join(lines)


def _analyze_single_group(
    group: ProductGroup,
    reviews: list[Review],
    llm: LLMClient,
    system_prompt: str,
    model_override: str | None = None,
) -> ProductAnalysis:
    """Analyze aggregated reviews for a product group."""
    if not reviews:
        return ProductAnalysis(
            product_group=group,
            review_summary=ReviewSummary(
                summary="Нет отзывов для анализа",
                trust_score=0.0,
            ),
        )

    # Build marketplace overview for context
    marketplace_info = []
    for offer in group.offers:
        marketplace_info.append(
            f"  {offer.marketplace}: {offer.price} руб. "
            f"(рейтинг {offer.rating}/5, {offer.review_count} отзывов)"
        )

    reviews_text = _format_reviews(reviews)
    user_message = (
        f"Товар: {group.canonical_name}\n"
        f"Представлен на маркетплейсах:\n" + "\n".join(marketplace_info) + "\n"
        f"Средний рейтинг: {group.avg_rating}/5 ({group.total_review_count} отзывов суммарно)\n\n"
        f"Отзывы со всех маркетплейсов ({len(reviews)} шт.):\n{reviews_text}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    try:
        result = llm.call_json(messages, temperature=0.3, max_tokens=1024, model_override=model_override)
        review_summary = ReviewSummary(
            pros=result.get("pros", []),
            cons=result.get("cons", []),
            summary=result.get("summary", ""),
            trust_score=min(1.0, max(0.0, result.get("trust_score", 0.5))),
        )
    except Exception as e:
        logger.warning(f"Review analysis failed for {group.group_id}: {e}")
        review_summary = ReviewSummary(
            summary=f"Рейтинг {group.avg_rating}/5 на основе {group.total_review_count} отзывов",
            trust_score=0.3,
        )

    return ProductAnalysis(product_group=group, review_summary=review_summary)


def run_review_analyzer(state: dict, llm: LLMClient, prompts_dir: Path, model_override: str | None = None) -> dict:
    """LangGraph node: analyze reviews for all product groups."""
    product_groups: list[ProductGroup] = state.get("product_groups", [])
    group_reviews: dict[str, list[Review]] = state.get("group_reviews", {})

    if not product_groups:
        return {
            "analyzed_products": [],
            "stage": WorkflowStage.REVIEWS_ANALYZED,
        }

    system_prompt = _load_prompt(prompts_dir)
    analyzed: list[ProductAnalysis] = []

    for group in product_groups:
        reviews = group_reviews.get(group.group_id, [])
        analysis = _analyze_single_group(group, reviews, llm, system_prompt, model_override)
        analyzed.append(analysis)
        logger.info(
            f"Analyzed reviews for {group.canonical_name} "
            f"({len(group.offers)} offers, {len(reviews)} reviews): "
            f"trust={analysis.review_summary.trust_score}",
            extra={"stage": "review_analyzer"},
        )

    stats = llm.get_usage_stats()
    return {
        "analyzed_products": analyzed,
        "stage": WorkflowStage.REVIEWS_ANALYZED,
        "llm_calls": stats["calls"],
        "total_tokens": stats["total_tokens"],
        "total_cost": stats["total_cost"],
    }
