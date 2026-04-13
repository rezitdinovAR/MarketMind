"""Mock data provider — loads products and reviews from JSON files."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from marketmind.models import Product, Review

logger = logging.getLogger("marketmind")

# Marketplace name mapping (normalized key -> json filename)
MARKETPLACE_FILES = {
    "ozon": "ozon_products.json",
    "wildberries": "wb_products.json",
    "yandex": "yandex_products.json",
}


class MockDataProvider:
    """Loads and searches mock product data from JSON files."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._data: dict[str, dict] = {}
        self._load_all()

    def _load_all(self) -> None:
        for marketplace, filename in MARKETPLACE_FILES.items():
            path = self.data_dir / filename
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self._data[marketplace] = json.load(f)
                logger.info(f"Loaded mock data for {marketplace}")
            else:
                logger.warning(f"Mock data file not found: {path}")
                self._data[marketplace] = {"categories": {}}

    def _match_category(self, marketplace: str, query: str) -> Optional[str]:
        """Find matching category by substring match."""
        categories = self._data.get(marketplace, {}).get("categories", {})
        query_lower = query.lower()

        # Direct match
        for cat_name in categories:
            if cat_name.lower() in query_lower or query_lower in cat_name.lower():
                return cat_name

        # Keyword-based fuzzy matching
        keyword_map = {
            "наушники": ["наушник", "airpods", "headphone", "earbuds", "tws"],
            "ноутбуки": ["ноутбук", "ноут", "laptop", "macbook", "vivobook"],
            "смартфоны": ["смартфон", "телефон", "phone", "iphone", "samsung galaxy", "xiaomi", "pixel"],
            "пылесосы": ["пылесос", "робот-пылесос", "робот пылесос", "vacuum", "roborock"],
            "телевизоры": ["телевизор", "тв", "tv", "oled", "qled", "телек"],
            "планшеты": ["планшет", "tablet", "ipad", "tab"],
            "умные часы": ["часы", "watch", "смарт-часы", "смарт часы", "фитнес-браслет", "фитнес браслет"],
            "кофемашины": ["кофемашин", "кофеварк", "coffee", "кофе машин", "эспрессо"],
        }
        for cat_name, keywords in keyword_map.items():
            if cat_name in categories:
                for kw in keywords:
                    if kw in query_lower:
                        return cat_name

        return None

    def search_products(
        self,
        marketplace: str,
        query: str,
        category: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        limit: int = 20,
    ) -> list[Product]:
        """Search products in mock data."""
        # Determine category
        search_cat = category or self._match_category(marketplace, query)
        if not search_cat:
            logger.info(f"No matching category for '{query}' on {marketplace}")
            return []

        raw_products = self._data.get(marketplace, {}).get("categories", {}).get(search_cat, [])

        products = []
        for p in raw_products:
            price = p["price"]
            if min_price and price < min_price:
                continue
            if max_price and price > max_price:
                continue

            products.append(Product(
                id=p["id"],
                name=p["name"],
                price=price,
                original_price=p.get("original_price"),
                marketplace=marketplace,
                url=p.get("url", ""),
                image_url=p.get("image_url"),
                rating=p.get("rating", 0),
                review_count=p.get("review_count", 0),
                in_stock=p.get("in_stock", True),
                seller_id=p.get("seller_id"),
                seller_name=p.get("seller_name"),
            ))

        return products[:limit]

    def get_reviews(
        self,
        product_id: str,
        marketplace: str,
        limit: int = 15,
    ) -> list[Review]:
        """Get reviews for a product from mock data.

        Applies filtering strategy:
        1. Prioritize reviews with text > 50 characters
        2. Sort by date (recent first)
        3. Balance verified/unverified purchases
        """
        categories = self._data.get(marketplace, {}).get("categories", {})
        for cat_products in categories.values():
            for p in cat_products:
                if p["id"] == product_id:
                    raw_reviews = p.get("reviews", [])

                    # Parse all reviews
                    all_reviews = []
                    for r in raw_reviews:
                        all_reviews.append(Review(
                            id=r["id"],
                            text=r["text"],
                            rating=r.get("rating", 5),
                            date=r.get("date", "2025-01-01"),
                            author=r.get("author"),
                            verified_purchase=r.get("verified_purchase", False),
                            helpful_count=r.get("helpful_count", 0),
                        ))

                    # Sort: prioritize text > 50 chars, then by date (recent first)
                    all_reviews.sort(
                        key=lambda r: (len(r.text) > 50, r.date),
                        reverse=True,
                    )

                    return all_reviews[:limit]
        return []

    def get_product_details(self, product_id: str, marketplace: str) -> dict | None:
        """Get full product details including attributes."""
        categories = self._data.get(marketplace, {}).get("categories", {})
        for cat_products in categories.values():
            for p in cat_products:
                if p["id"] == product_id:
                    return {
                        "id": p["id"],
                        "name": p["name"],
                        "full_description": p.get("full_description", p["name"]),
                        "price": p["price"],
                        "original_price": p.get("original_price"),
                        "rating": p.get("rating", 0),
                        "review_count": p.get("review_count", 0),
                        "url": p.get("url", ""),
                        "image_url": p.get("image_url"),
                        "image_urls": p.get("image_urls", [p.get("image_url", "")] if p.get("image_url") else []),
                        "in_stock": p.get("in_stock", True),
                        "attributes": p.get("attributes", {}),
                        "seller_id": p.get("seller_id"),
                        "seller_name": p.get("seller_name"),
                        "delivery_info": p.get("delivery_info", "1-3 дня"),
                    }
        return None

    def get_seller_info(self, seller_id: str, marketplace: str) -> dict | None:
        """Get seller information from mock data."""
        categories = self._data.get(marketplace, {}).get("categories", {})
        for cat_products in categories.values():
            for p in cat_products:
                if p.get("seller_id") == seller_id:
                    seller_data = p.get("seller_info", {})
                    return {
                        "id": p["seller_id"],
                        "name": p.get("seller_name", "Unknown"),
                        "rating": seller_data.get("rating", p.get("rating", 4.0)),
                        "review_count": seller_data.get("review_count", 100),
                        "registration_date": seller_data.get("registration_date", "2020-01-01"),
                        "is_official": seller_data.get("is_official",
                            "official" in p.get("seller_name", "").lower()
                            or "store" in p.get("seller_name", "").lower()),
                        "return_policy": seller_data.get("return_policy", "14 дней"),
                        "delivery_speed": seller_data.get("delivery_speed", "1-3 дня"),
                    }
        return None

    def get_available_categories(self, marketplace: str) -> list[str]:
        """List available categories for a marketplace."""
        return list(self._data.get(marketplace, {}).get("categories", {}).keys())
