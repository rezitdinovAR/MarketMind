"""Recommender — generates final top-3 recommendation with explanation."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from marketmind.llm_client import LLMClient
from marketmind.observability import metrics
from marketmind.models import (
    ProductAnalysis,
    QuerySpec,
    RankedProduct,
    Recommendation,
    WorkflowStage,
)

logger = logging.getLogger("marketmind")


FALLBACK_SYSTEM_PROMPT = (
    "Сформируй рекомендацию топ-3 товаров. "
    "Верни JSON с top3, explanation и confidence."
)


def _load_prompt(prompts_dir: Path) -> str:
    path = prompts_dir / "recommendation.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return FALLBACK_SYSTEM_PROMPT


def _build_recommendation_input(analyzed: list[ProductAnalysis], query_spec: QuerySpec) -> str:
    lines = [
        f"Запрос пользователя: {query_spec.raw_query}",
        f"Категория: {query_spec.category}",
        f"Бюджет: до {query_spec.budget_max} руб." if query_spec.budget_max else "Бюджет: не указан",
        f"Обязательные: {', '.join(query_spec.must_have) or 'не указаны'}",
        "",
        "--- Товары (сгруппированы по модели, отсортированы по оценке) ---",
    ]

    sorted_products = sorted(
        analyzed,
        key=lambda a: a.fit_score * 0.6 + a.value_score * 0.4,
        reverse=True,
    )

    for a in sorted_products:
        g = a.product_group
        rs = a.review_summary

        lines.append(f"\nID: {g.group_id}")
        lines.append(f"Модель: {g.canonical_name}")

        # Prices across marketplaces
        prices_str = " | ".join(
            f"{o.marketplace}: {o.price} руб." for o in g.offers
        )
        lines.append(f"Цены: {prices_str}")
        lines.append(f"Лучшая цена: {g.best_price} руб. ({g.best_marketplace})")

        lines.append(f"Средний рейтинг: {g.avg_rating}/5 ({g.total_review_count} отзывов)")
        lines.append(f"Оценка цена/качество: {a.value_score}")
        lines.append(f"Соответствие запросу: {a.fit_score}")
        if rs.pros:
            lines.append(f"Плюсы: {'; '.join(rs.pros)}")
        if rs.cons:
            lines.append(f"Минусы: {'; '.join(rs.cons)}")

    return "\n".join(lines)


def _validate_recommendation(result: dict, analyzed: list[ProductAnalysis]) -> bool:
    valid_ids = {a.product_group.group_id for a in analyzed}
    for item in result.get("top3", []):
        if item.get("product_id") not in valid_ids:
            return False
    return True


def _check_price_consistency(
    explanation: str,
    analyzed: list[ProductAnalysis],
    tolerance: float = 0.05,
) -> str:
    """Validate prices mentioned in the LLM explanation against real data.

    If a price in the text differs from the actual best price by more than
    the tolerance (default 5%), it gets replaced with the correct value.

    Returns corrected explanation text.
    """
    # Build lookup: product name -> best_price
    name_to_price: dict[str, int] = {}
    for a in analyzed:
        g = a.product_group
        # Store by canonical name and by shortened forms
        name_to_price[g.canonical_name.lower()] = g.best_price
        # Also store partial key (first 3 words) for fuzzy matching
        words = g.canonical_name.split()
        if len(words) >= 2:
            name_to_price[" ".join(words[:3]).lower()] = g.best_price

    corrected = explanation
    corrections_made = 0

    # Find all price mentions in the text: "12 345 руб" or "12345 руб" or "12,345₽"
    price_pattern = re.compile(r"(\d[\d\s,.]*\d)\s*(?:руб\.?|₽)", re.IGNORECASE)

    for match in price_pattern.finditer(explanation):
        raw_price_str = match.group(1)
        # Normalize: remove spaces, commas, dots used as thousands separators
        clean_str = re.sub(r"[\s,.]", "", raw_price_str)
        try:
            mentioned_price = int(clean_str)
        except ValueError:
            continue

        # Check against all known best prices
        for name, actual_price in name_to_price.items():
            if actual_price == 0:
                continue
            diff_ratio = abs(mentioned_price - actual_price) / actual_price
            if diff_ratio <= tolerance:
                break  # price is close enough
            # If the mentioned price is close to an actual price but wrong, fix it
            if 0.5 < (mentioned_price / actual_price) < 2.0 and diff_ratio > tolerance:
                corrected = corrected.replace(
                    raw_price_str,
                    f"{actual_price:,}".replace(",", " "),
                    1,
                )
                corrections_made += 1
                break

    if corrections_made:
        logger.info(f"Price consistency: corrected {corrections_made} price(s) in explanation")

    return corrected


def run_recommender(state: dict, llm: LLMClient, prompts_dir: Path, model_override: str | None = None) -> dict:
    """LangGraph node: generate final recommendation."""
    import time as _time
    _start = _time.time()
    _regenerate_count = 0
    _validation_failures = 0

    analyzed: list[ProductAnalysis] = state.get("analyzed_products", [])
    query_spec: QuerySpec = state.get("query_spec")

    if not analyzed or not query_spec:
        return {
            "recommendation": Recommendation(
                explanation="Не удалось сформировать рекомендацию: нет данных для анализа.",
                user_query=query_spec.raw_query if query_spec else "",
                confidence=0.0,
            ),
            "stage": WorkflowStage.RECOMMENDED,
        }

    system_prompt = _load_prompt(prompts_dir)
    user_input = _build_recommendation_input(analyzed, query_spec)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    group_map = {a.product_group.group_id: a for a in analyzed}

    for attempt in range(2):
        if attempt > 0:
            _regenerate_count += 1
        try:
            result = llm.call_json(messages, temperature=0.4, max_tokens=2048, model_override=model_override)

            if not _validate_recommendation(result, analyzed):
                _validation_failures += 1
                logger.warning("Recommendation validation failed, retrying")
                messages.append({"role": "assistant", "content": str(result)})
                messages.append({
                    "role": "user",
                    "content": (
                        "Некоторые product_id в ответе не совпадают с реальными. "
                        "Используй ТОЛЬКО id из списка товаров (group_id). Повтори."
                    ),
                })
                continue

            # Length check: explanation must be > 100 chars
            explanation = result.get("explanation", "")
            if len(explanation) < 100:
                logger.warning(f"Explanation too short ({len(explanation)} chars), retrying")
                messages.append({"role": "assistant", "content": str(result)})
                messages.append({
                    "role": "user",
                    "content": "Explanation слишком короткий. Напиши развёрнутое объяснение (минимум 200 слов) почему именно эти товары лучше всего подходят.",
                })
                continue

            # Hallucination check: verify mentioned product names exist
            known_names = {a.product_group.canonical_name.lower() for a in analyzed}
            known_ids = {a.product_group.group_id for a in analyzed}
            top3_data = result.get("top3", [])
            for item in top3_data:
                pid = item.get("product_id", "")
                if pid and pid not in known_ids:
                    logger.warning(f"Hallucinated product_id in recommendation: {pid}")
                    # This case is already handled by _validate_recommendation above
                    break

            top3 = []
            for item in result.get("top3", [])[:3]:
                pid = item["product_id"]
                pa = group_map.get(pid)
                if pa:
                    top3.append(RankedProduct(
                        rank=item.get("rank", len(top3) + 1),
                        product_group=pa.product_group,
                        review_summary=pa.review_summary,
                        final_score=min(1.0, max(0.0, item.get("final_score", 0.5))),
                        fit_explanation=item.get("fit_explanation", ""),
                        main_advantage=item.get("main_advantage", ""),
                        main_caveat=item.get("main_caveat", ""),
                    ))

            # Guardrail: fix any hallucinated prices in the explanation
            raw_explanation = result.get("explanation", "")
            checked_explanation = _check_price_consistency(raw_explanation, analyzed)

            recommendation = Recommendation(
                top3=top3,
                explanation=checked_explanation,
                confidence=min(1.0, max(0.0, result.get("confidence", 0.5))),
                user_query=query_spec.raw_query,
            )

            logger.info(
                f"Recommendation generated: {len(top3)} models, confidence={recommendation.confidence}",
                extra={"stage": "recommender"},
            )

            # Record metrics
            metrics.observe("recommendation_latency_seconds", _time.time() - _start)
            if recommendation:
                metrics.observe("recommendation_confidence", recommendation.confidence)
            if _regenerate_count > 0:
                metrics.inc("recommendation_regenerate_count", value=_regenerate_count)
            if _validation_failures > 0:
                metrics.inc("recommendation_validation_failures", value=_validation_failures)

            stats = llm.get_usage_stats()
            return {
                "recommendation": recommendation,
                "stage": WorkflowStage.RECOMMENDED,
                "llm_calls": stats["calls"],
                "total_tokens": stats["total_tokens"],
                "total_cost": stats["total_cost"],
            }

        except Exception as e:
            logger.error(f"Recommendation attempt {attempt + 1} failed: {e}")

    # Fallback: template-based
    sorted_products = sorted(
        analyzed,
        key=lambda a: a.fit_score * 0.6 + a.value_score * 0.4,
        reverse=True,
    )
    top3 = []
    for i, a in enumerate(sorted_products[:3]):
        top3.append(RankedProduct(
            rank=i + 1,
            product_group=a.product_group,
            review_summary=a.review_summary,
            final_score=round(a.fit_score * 0.6 + a.value_score * 0.4, 2),
            fit_explanation=f"Рейтинг {a.product_group.avg_rating}/5, лучшая цена {a.product_group.best_price} руб.",
            main_advantage=a.review_summary.pros[0] if a.review_summary.pros else "Хороший рейтинг",
            main_caveat=a.review_summary.cons[0] if a.review_summary.cons else "Нет существенных минусов",
        ))

    # Record metrics (fallback path)
    fallback_recommendation = Recommendation(
        top3=top3,
        explanation="Рекомендация составлена автоматически на основе рейтинга, цены и отзывов.",
        confidence=0.3,
        user_query=query_spec.raw_query,
    )
    metrics.observe("recommendation_latency_seconds", _time.time() - _start)
    if fallback_recommendation:
        metrics.observe("recommendation_confidence", fallback_recommendation.confidence)
    if _regenerate_count > 0:
        metrics.inc("recommendation_regenerate_count", value=_regenerate_count)
    if _validation_failures > 0:
        metrics.inc("recommendation_validation_failures", value=_validation_failures)

    stats = llm.get_usage_stats()
    return {
        "recommendation": fallback_recommendation,
        "stage": WorkflowStage.RECOMMENDED,
        "llm_calls": stats["calls"],
        "total_tokens": stats["total_tokens"],
        "total_cost": stats["total_cost"],
    }
