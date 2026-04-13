"""ProductSearcher — searches products across marketplaces, groups same models."""

from __future__ import annotations

import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher

from marketmind.models import (
    MarketplaceOffer,
    Product,
    ProductGroup,
    Review,
    WorkflowStage,
)
from marketmind.tools.mock_provider import MockDataProvider
from marketmind.tools.tool_wrapper import execute_tool, ToolResult

logger = logging.getLogger("marketmind")

# Words that describe color/form factor but not the model itself
_NOISE_WORDS = {
    "полноразмерные", "беспроводные", "беспроводной", "проводные", "проводной",
    "чёрные", "черные", "белые", "серые", "синие", "красные", "зелёные",
    "чёрный", "черный", "белый", "серый", "серебристый", "золотой",
    "робот-пылесос", "робот", "пылесос",
    "смартфон", "ноутбук", "планшет", "телевизор",
    "автоматическая", "автоматический", "кофемашина",
    "умные", "смарт",
}


def _extract_model_key(name: str) -> str:
    """Extract the core brand+model identifier for grouping.

    'Sony WH-1000XM5 Полноразмерные беспроводные' → 'sony wh-1000xm5'
    'Sony WH-1000XM5 Чёрные'                      → 'sony wh-1000xm5'
    """
    words = name.lower().split()
    core = [w for w in words if w not in _NOISE_WORDS]
    # Keep only brand + model tokens (first 3 significant words usually enough)
    key = " ".join(core[:3])
    # Collapse whitespace and punctuation for matching
    key = re.sub(r"[(),]", "", key).strip()
    return key


def _are_same_model(name_a: str, name_b: str) -> bool:
    """Determine whether two product names refer to the same model."""
    key_a = _extract_model_key(name_a)
    key_b = _extract_model_key(name_b)
    # Exact match on model key
    if key_a == key_b:
        return True
    # Fuzzy: one key is a prefix of the other, or high similarity
    if key_a.startswith(key_b) or key_b.startswith(key_a):
        return True
    return SequenceMatcher(None, key_a, key_b).ratio() > 0.78


def _group_products(
    all_products: list[Product],
    all_reviews: dict[str, list[Review]],
) -> tuple[list[ProductGroup], dict[str, list[Review]]]:
    """Group products that are the same model across marketplaces."""
    groups: list[list[Product]] = []
    assigned: set[int] = set()

    for i, p in enumerate(all_products):
        if i in assigned:
            continue
        group = [p]
        assigned.add(i)
        for j in range(i + 1, len(all_products)):
            if j in assigned:
                continue
            if _are_same_model(p.name, all_products[j].name):
                group.append(all_products[j])
                assigned.add(j)
        groups.append(group)

    # Build ProductGroup objects
    product_groups: list[ProductGroup] = []
    group_reviews: dict[str, list[Review]] = {}

    for idx, group in enumerate(groups):
        # Canonical name: shortest name in the group (usually the cleanest)
        canonical = min(group, key=lambda p: len(p.name)).name

        offers = []
        combined_reviews: list[Review] = []

        for p in group:
            offers.append(MarketplaceOffer(
                marketplace=p.marketplace,
                product_id=p.id,
                price=p.price,
                original_price=p.original_price,
                url=p.url,
                seller_name=p.seller_name,
                rating=p.rating,
                review_count=p.review_count,
            ))
            # Aggregate reviews from all marketplaces
            if p.id in all_reviews:
                combined_reviews.extend(all_reviews[p.id])

        # Sort offers by price (cheapest first)
        offers.sort(key=lambda o: o.price)
        best = offers[0]

        group_id = f"grp_{idx:03d}"
        avg_rating = round(sum(o.rating for o in offers) / len(offers), 2)
        total_reviews = sum(o.review_count for o in offers)

        # Merge attributes from all products in the group (first non-empty wins)
        merged_attrs = {}
        for p in group:
            if hasattr(p, 'attributes') and p.attributes:
                for k, v in p.attributes.items():
                    if k not in merged_attrs:
                        merged_attrs[k] = v

        pg = ProductGroup(
            group_id=group_id,
            canonical_name=canonical,
            offers=offers,
            best_price=best.price,
            best_marketplace=best.marketplace,
            avg_rating=avg_rating,
            total_review_count=total_reviews,
            attributes=merged_attrs,
        )
        product_groups.append(pg)

        # Deduplicate reviews by id
        seen_ids: set[str] = set()
        unique_reviews: list[Review] = []
        for r in combined_reviews:
            if r.id not in seen_ids:
                seen_ids.add(r.id)
                unique_reviews.append(r)
        group_reviews[group_id] = unique_reviews

    return product_groups, group_reviews


def run_product_searcher(
    state: dict,
    mock_provider: MockDataProvider,
    enabled_sources: dict[str, bool],
    max_results_total: int = 10,
    min_rating: float = 3.5,
    max_reviews_per_product: int = 15,
) -> dict:
    """LangGraph node: search products, group same models, collect reviews."""
    query_spec = state.get("query_spec")
    if not query_spec:
        return {
            "product_groups": [],
            "stage": WorkflowStage.PRODUCTS_FOUND,
            "errors": ["No query_spec available for search"],
        }

    category = query_spec.category
    raw_query = query_spec.raw_query
    budget_max = query_spec.budget_max
    budget_min = query_spec.budget_min

    all_products: list[Product] = []
    all_reviews: dict[str, list[Review]] = {}
    errors: list[str] = []

    # Respect marketplace priority from user preferences
    priority_order = query_spec.marketplace_priority if hasattr(query_spec, 'marketplace_priority') and query_spec.marketplace_priority else list(enabled_sources.keys())
    # Build ordered list: priority items first, then any remaining enabled sources
    ordered_marketplaces = []
    for mp in priority_order:
        if mp in enabled_sources and enabled_sources[mp]:
            ordered_marketplaces.append(mp)
    for mp in enabled_sources:
        if mp not in ordered_marketplaces and enabled_sources[mp]:
            ordered_marketplaces.append(mp)

    def _search_single_marketplace(marketplace):
        """Search a single marketplace and return products + reviews."""
        mp_products = []
        mp_reviews = {}
        mp_errors = []

        try:
            search_result = execute_tool(
                tool_name=f"search_{marketplace}",
                handler=mock_provider.search_products,
                params={
                    "marketplace": marketplace,
                    "query": raw_query if not category else category,
                    "category": category,
                    "min_price": budget_min,
                    "max_price": budget_max,
                },
                timeout_sec=10,
                max_retries=2,
            )

            if not search_result.success or not search_result.data:
                if search_result.error:
                    mp_errors.append(f"Search error on {marketplace}: {search_result.error}")
                return mp_products, mp_reviews, mp_errors

            products = [p for p in search_result.data if p.rating >= min_rating]

            for product in products:
                # Fetch reviews
                review_result = execute_tool(
                    tool_name=f"get_reviews_{marketplace}",
                    handler=mock_provider.get_reviews,
                    params={"product_id": product.id, "marketplace": marketplace, "limit": max_reviews_per_product},
                    timeout_sec=5,
                    max_retries=1,
                )
                if review_result.success and review_result.data:
                    mp_reviews[product.id] = review_result.data

                # Fetch product details for attributes
                details_result = execute_tool(
                    tool_name=f"get_details_{marketplace}",
                    handler=mock_provider.get_product_details,
                    params={"product_id": product.id, "marketplace": marketplace},
                    timeout_sec=5,
                    max_retries=1,
                )
                if details_result.success and details_result.data:
                    product.attributes = details_result.data.get("attributes", {})

                # Fetch seller info
                if product.seller_id:
                    seller_result = execute_tool(
                        tool_name=f"get_seller_{marketplace}",
                        handler=mock_provider.get_seller_info,
                        params={"seller_id": product.seller_id, "marketplace": marketplace},
                        timeout_sec=5,
                        max_retries=1,
                    )
                    if seller_result.success and seller_result.data:
                        if not product.seller_name:
                            product.seller_name = seller_result.data.get("name", product.seller_name)

            mp_products = products
            logger.info(f"Found {len(products)} products on {marketplace}",
                        extra={"stage": "product_searcher"})
        except Exception as e:
            logger.warning(f"Search failed for {marketplace}: {e}")
            mp_errors.append(f"Search error on {marketplace}: {e}")

        return mp_products, mp_reviews, mp_errors

    # Parallel search across marketplaces
    with ThreadPoolExecutor(max_workers=len(ordered_marketplaces)) as executor:
        futures = {
            executor.submit(_search_single_marketplace, mp): mp
            for mp in ordered_marketplaces
        }
        for future in as_completed(futures):
            mp_products, mp_reviews, mp_errors = future.result()
            all_products.extend(mp_products)
            all_reviews.update(mp_reviews)
            errors.extend(mp_errors)

    # Group same models across marketplaces
    product_groups, group_reviews = _group_products(all_products, all_reviews)

    # Sort by avg rating, limit
    product_groups.sort(key=lambda g: (g.avg_rating, g.total_review_count), reverse=True)
    product_groups = product_groups[:max_results_total]

    # Keep only reviews for selected groups
    selected_ids = {g.group_id for g in product_groups}
    group_reviews = {gid: revs for gid, revs in group_reviews.items() if gid in selected_ids}

    logger.info(
        f"Grouped into {len(product_groups)} unique models from {len(all_products)} products",
        extra={"stage": "product_searcher"},
    )

    result = {
        "product_groups": product_groups,
        "group_reviews": group_reviews,
        "stage": WorkflowStage.PRODUCTS_FOUND,
    }
    if errors:
        result["errors"] = errors
    return result
