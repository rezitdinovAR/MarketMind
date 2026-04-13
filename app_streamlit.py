"""Streamlit UI for MarketMind."""

from __future__ import annotations

import streamlit as st

from marketmind.config import load_settings
from marketmind.models import Recommendation, RankedProduct
from marketmind.observability import setup_logger
from marketmind.orchestrator import Orchestrator

# --- Page config ---
st.set_page_config(
    page_title="MarketMind",
    page_icon="🛒",
    layout="wide",
)

# --- Init ---

@st.cache_resource
def get_orchestrator() -> Orchestrator:
    settings = load_settings()
    setup_logger(level=settings.app.log_level, log_dir=settings.get_logs_path(), debug=settings.app.debug)
    return Orchestrator(settings)


def render_product_card(rp: RankedProduct) -> None:
    """Render a single product group recommendation card."""
    g = rp.product_group
    rs = rp.review_summary

    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rp.rank, "")

    st.markdown(f"### {medal} #{rp.rank} — {g.canonical_name}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Лучшая цена", f"{g.best_price:,} ₽")
    col2.metric("Средний рейтинг", f"⭐ {g.avg_rating}/5")
    col3.metric("Отзывов", f"{g.total_review_count:,}")

    if rp.fit_explanation:
        st.info(f"**Почему подходит:** {rp.fit_explanation}")

    adv_col, cav_col = st.columns(2)
    if rp.main_advantage:
        adv_col.success(f"✅ {rp.main_advantage}")
    if rp.main_caveat:
        cav_col.warning(f"⚠️ {rp.main_caveat}")

    # Marketplace price comparison table
    st.markdown("**Цены на маркетплейсах:**")
    for offer in g.offers:
        is_best = offer.price == g.best_price
        marker = " ← лучшая цена" if is_best else ""
        discount = ""
        if offer.original_price and offer.original_price > offer.price:
            pct = round((1 - offer.price / offer.original_price) * 100)
            discount = f" ~~{offer.original_price:,} ₽~~ (-{pct}%)"

        st.markdown(
            f"- **{offer.marketplace.capitalize()}**: "
            f"**{offer.price:,} ₽**{discount}{marker} "
            f"| {offer.rating}/5 ({offer.review_count} отзывов) "
            f"| [{offer.seller_name or 'продавец'}]({offer.url})"
        )

    with st.expander("Подробнее об отзывах (со всех маркетплейсов)"):
        if rs.pros:
            st.markdown("**Плюсы:**")
            for pro in rs.pros:
                st.markdown(f"- ✅ {pro}")
        if rs.cons:
            st.markdown("**Минусы:**")
            for con in rs.cons:
                st.markdown(f"- ❌ {con}")
        if rs.summary:
            st.markdown(f"**Резюме:** {rs.summary}")
        st.caption(f"Доверие к отзывам: {rs.trust_score:.0%}")

    st.divider()


def main() -> None:
    st.title("🛒 MarketMind")
    st.caption("AI-ассистент по подбору товаров на маркетплейсах")

    # Check API key
    settings = load_settings()
    if not settings.llm.api_key:
        st.error(
            "⚠️ **DEEPSEEK_API_KEY не настроен.** "
            "Создайте файл `.env` в корне проекта с содержимым:\n\n"
            "```\nDEEPSEEK_API_KEY=sk-your-key\n```"
        )
        st.stop()

    orchestrator = get_orchestrator()

    # Chat history (display) + pipeline history (context for QueryAnalyzer)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pipeline_history" not in st.session_state:
        st.session_state.pipeline_history = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_query = st.chat_input("Опишите, какой товар вы ищете...")

    if user_query:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.session_state.pipeline_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Process — pass pipeline_history (current search conversation only)
        with st.chat_message("assistant"):
            with st.spinner("Анализирую запрос и ищу товары..."):
                result = orchestrator.run(user_query, chat_history=st.session_state.pipeline_history)

            query_spec = result.get("query_spec")
            recommendation: Recommendation | None = result.get("recommendation")
            errors = result.get("errors", [])

            # Clarification needed — keep pipeline_history for next turn
            if query_spec and query_spec.needs_clarification:
                msg = "Мне нужно уточнить ваш запрос:\n\n"
                for q in query_spec.clarification_questions:
                    msg += f"- {q}\n"
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.session_state.pipeline_history.append({"role": "assistant", "content": msg})

            # No results — reset pipeline for fresh search
            elif not result.get("product_groups"):
                msg = (
                    "К сожалению, по вашему запросу ничего не найдено. "
                    "Попробуйте расширить критерии или изменить запрос."
                )
                st.warning(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.session_state.pipeline_history.clear()

            # Show recommendations
            elif recommendation and recommendation.top3:
                groups_count = len(result.get("product_groups", []))
                st.markdown(
                    f"**Найдено моделей:** {groups_count} | "
                    f"**Проанализировано:** {len(result.get('analyzed_products', []))}"
                )

                for rp in recommendation.top3:
                    render_product_card(rp)

                # Explanation
                if recommendation.explanation:
                    st.markdown("### 📝 Общий анализ")
                    st.markdown(recommendation.explanation)

                # Confidence
                st.progress(recommendation.confidence, text=f"Уверенность: {recommendation.confidence:.0%}")

                # Stats (only shown when debug info is enabled)
                if settings.ui.show_debug_info:
                    llm_calls = result.get("llm_calls", 0)
                    total_cost = result.get("total_cost", 0)
                    with st.expander("📊 Статистика запроса"):
                        stat_cols = st.columns(3)
                        stat_cols[0].metric("LLM вызовов", llm_calls)
                        stat_cols[1].metric("Стоимость", f"${total_cost:.4f}")
                        stat_cols[2].metric("Уникальных моделей", groups_count)

                        if query_spec:
                            st.json({
                                "category": query_spec.category,
                                "budget_max": query_spec.budget_max,
                                "must_have": query_spec.must_have,
                                "nice_to_have": query_spec.nice_to_have,
                            })

                # Save summary for chat history and reset pipeline for fresh search
                summary = f"Рекомендую {len(recommendation.top3)} моделей:\n\n"
                for rp in recommendation.top3:
                    g = rp.product_group
                    prices = ", ".join(f"{o.marketplace}: {o.price:,}₽" for o in g.offers)
                    summary += f"{rp.rank}. **{g.canonical_name}** — от {g.best_price:,} ₽ ({prices})\n"
                st.session_state.messages.append({"role": "assistant", "content": summary})
                st.session_state.pipeline_history.clear()

            if errors:
                with st.expander("⚠️ Предупреждения"):
                    for err in errors:
                        st.warning(err)

        # Disclaimer
        st.caption(
            "⚠️ MarketMind — AI-ассистент. Рекомендации основаны на автоматическом анализе "
            "и могут содержать неточности. Перед покупкой проверьте информацию на сайте маркетплейса. "
            "Цены и наличие могут измениться."
        )


if __name__ == "__main__":
    main()
