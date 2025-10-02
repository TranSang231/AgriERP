# models/article.py
from django.db import models
from base.models import TimeStampedModel
from .promotion import Promotion
from .product import Product

class PromotionItem(TimeStampedModel):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name="promotion_items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="promotion_items"
    )
    quantity_limit =  models.FloatField(default=0.0, blank=True)
    quantity_limit_by_customer =  models.FloatField(default=0.0, blank=True)
    # discount percent
    discount = models.FloatField(default=0.0, blank=True)

    class Meta:
        db_table = "ecommerce_promotion_items"
        ordering = ["-created_at"]
