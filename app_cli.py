"""CLI entry point for MarketMind."""

from __future__ import annotations

import sys

from marketmind.config import load_settings
from marketmind.observability import setup_logger
from marketmind.orchestrator import Orchestrator

DISCLAIMER = (
    "\n--- MarketMind AI ---\n"
    "AI-ассистент по подбору товаров на маркетплейсах.\n"
    "Введите запрос на естественном языке (или 'выход' для завершения).\n"
)

WARNING = (
    "MarketMind — AI-ассистент. Рекомендации основаны на автоматическом анализе "
    "и могут содержать неточности. Перед покупкой проверьте информацию на сайте маркетплейса."
)


def format_recommendation(state: dict, show_debug: bool = False) -> str:
    """Format final state into readable output."""
    query_spec = state.get("query_spec")
    recommendation = state.get("recommendation")
    errors = state.get("errors", [])

    lines: list[str] = []

    # Clarification needed
    if query_spec and query_spec.needs_clarification:
        lines.append("\nНужно уточнение:")
        for q in query_spec.clarification_questions:
            lines.append(f"  - {q}")
        return "\n".join(lines)

    # No results
    groups = state.get("product_groups", [])
    if not groups:
        lines.append("\nК сожалению, по вашему запросу ничего не найдено.")
        lines.append("Попробуйте расширить критерии поиска.")
        return "\n".join(lines)

    # Show recommendation
    if recommendation and recommendation.top3:
        lines.append(f"\n{'='*60}")
        lines.append(f"  РЕКОМЕНДАЦИИ ПО ЗАПРОСУ: {recommendation.user_query}")
        lines.append(f"{'='*60}")

        for rp in recommendation.top3:
            g = rp.product_group
            lines.append(f"\n  #{rp.rank} {g.canonical_name}")
            lines.append(f"     Лучшая цена: {g.best_price:,} руб. ({g.best_marketplace})")
            lines.append(f"     Рейтинг: {g.avg_rating}/5 ({g.total_review_count} отзывов)")

            # Price comparison
            lines.append("     Цены на маркетплейсах:")
            for offer in g.offers:
                best_mark = " <-- лучшая" if offer.price == g.best_price else ""
                lines.append(f"       {offer.marketplace:12s}  {offer.price:>7,} руб.  "
                             f"({offer.rating}/5, {offer.review_count} отз.){best_mark}")

            if rp.fit_explanation:
                lines.append(f"     Почему: {rp.fit_explanation}")
            if rp.main_advantage:
                lines.append(f"     + {rp.main_advantage}")
            if rp.main_caveat:
                lines.append(f"     - {rp.main_caveat}")

            # Reviews
            rs = rp.review_summary
            if rs.pros:
                lines.append(f"     Плюсы: {'; '.join(rs.pros[:3])}")
            if rs.cons:
                lines.append(f"     Минусы: {'; '.join(rs.cons[:3])}")

        if recommendation.explanation:
            lines.append(f"\n{'─'*60}")
            lines.append(f"  {recommendation.explanation}")

        lines.append(f"\n  Уверенность: {recommendation.confidence:.0%}")

    # Stats (only shown when debug info is enabled)
    if show_debug:
        llm_calls = state.get("llm_calls", 0)
        total_cost = state.get("total_cost", 0)
        if llm_calls:
            lines.append(f"\n  [LLM: {llm_calls} вызовов, ${total_cost:.4f}]")

    # Errors
    if errors:
        lines.append(f"\n  Предупреждения: {'; '.join(errors)}")

    lines.append(f"\n  {WARNING}")
    return "\n".join(lines)


def main() -> None:
    settings = load_settings()
    logger = setup_logger(level=settings.app.log_level, log_dir=settings.get_logs_path(), debug=settings.app.debug)

    if not settings.llm.api_key:
        print("ОШИБКА: DEEPSEEK_API_KEY не установлен.")
        print("Создайте файл .env с содержимым: DEEPSEEK_API_KEY=sk-your-key")
        sys.exit(1)

    orchestrator = Orchestrator(settings)
    print(DISCLAIMER)

    chat_history: list[dict] = []

    while True:
        try:
            query = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо свидания!")
            break

        if not query:
            continue
        if query.lower() in ("выход", "exit", "quit", "q"):
            print("До свидания!")
            break
        if query.lower() in ("новый", "сброс", "reset"):
            chat_history.clear()
            print("Диалог сброшен. Введите новый запрос.")
            continue

        chat_history.append({"role": "user", "content": query})

        print("\nОбработка запроса...")
        result = orchestrator.run(query, chat_history=chat_history)
        output = format_recommendation(result, show_debug=settings.ui.show_debug_info)
        print(output)

        # Save assistant response to history for context in next turn
        query_spec = result.get("query_spec")
        if query_spec and query_spec.needs_clarification:
            clarification_text = "Мне нужно уточнить:\n" + "\n".join(
                f"- {q}" for q in query_spec.clarification_questions
            )
            chat_history.append({"role": "assistant", "content": clarification_text})
        else:
            # Successful result — reset history for next product search
            chat_history.clear()


if __name__ == "__main__":
    main()
