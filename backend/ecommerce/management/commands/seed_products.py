from django.core.management.base import BaseCommand
from django.db import transaction
from typing import List

from contents.models import ShortContent, LongContent
from ecommerce.models import Product, ProductCategory


DEFAULT_CATEGORY_NAMES: List[str] = [
    "Fruits",
    "Vegetables",
    "Beverages",
    "Snacks",
    "Dairy",
]

DEFAULT_UNITS: List[str] = ["Kg", "Pack", "Box", "Bottle", "Piece"]

DEFAULT_PRODUCTS: List[dict] = [
    {"name": "Apple Fuji", "desc": "Fresh, sweet Fuji apples.", "price": 120000, "unit": "Kg"},
    {"name": "Orange", "desc": "Juicy and rich in vitamin C.", "price": 90000, "unit": "Kg"},
    {"name": "Milk 1L", "desc": "Pasteurized whole milk.", "price": 35000, "unit": "Bottle"},
    {"name": "Potato", "desc": "Good for fries and mash.", "price": 45000, "unit": "Kg"},
    {"name": "Almonds", "desc": "Crunchy healthy snack.", "price": 250000, "unit": "Pack"},
]


class Command(BaseCommand):
    help = "Seed sample product categories and products for the shop"

    def add_arguments(self, parser):
        parser.add_argument("--categories", type=int, default=5, help="Number of categories to create (default 5)")
        parser.add_argument("--products", type=int, default=20, help="Number of products to create (default 20)")

    @transaction.atomic
    def handle(self, *args, **options):
        num_categories: int = options["categories"]
        num_products: int = options["products"]

        categories = self._ensure_categories(num_categories)
        created = self._ensure_products(num_products, categories)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(categories)} categories and {created} products."
        ))

    def _ensure_categories(self, num: int) -> List[ProductCategory]:
        categories: List[ProductCategory] = []
        base_names = DEFAULT_CATEGORY_NAMES.copy()
        # Create or reuse by name ShortContent
        for i in range(num):
            label = base_names[i % len(base_names)]
            sc = ShortContent.objects.filter(origin=label).first()
            if sc is None:
                sc = ShortContent.objects.create(origin=label)
            category = ProductCategory.objects.filter(name=sc).first()
            if category is None:
                category = ProductCategory.objects.create(name=sc, description=f"{label} category")
            categories.append(category)
        return categories

    def _ensure_products(self, num: int, categories: List[ProductCategory]) -> int:
        created = 0
        base_products = DEFAULT_PRODUCTS.copy()
        for i in range(num):
            spec = base_products[i % len(base_products)]
            name_text = spec["name"] if i < len(base_products) else f"Sample Product {i+1}"
            desc_text = spec.get("desc", "")
            price_value = spec.get("price", 10000)
            unit_text = spec.get("unit", DEFAULT_UNITS[i % len(DEFAULT_UNITS)])

            name_sc = ShortContent.objects.create(origin=name_text)
            desc_lc = LongContent.objects.create(origin=desc_text)
            unit_sc = ShortContent.objects.create(origin=unit_text)

            product = Product.objects.create(
                name=name_sc,
                description=desc_lc,
                price=price_value,
                unit=unit_sc,
                in_stock=50,
                weight=1.0,
                length=10.0,
                width=8.0,
                height=8.0,
                tax_rate=8.0,
            )

            # Assign one category deterministically
            if categories:
                product.categories.add(categories[i % len(categories)])

            created += 1

        return created


