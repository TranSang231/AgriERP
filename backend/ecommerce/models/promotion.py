from django.db import models
from base.models import TimeStampedModel
from .product import Product

class Promotion(TimeStampedModel):
    name = models.CharField(max_length=120, blank=True)
    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)
    # type of promotion: 'discount' for selected products via PromotionItem,
    # 'voucher' for applying a percent to all selected products
    TYPE_DISCOUNT = "discount"
    TYPE_VOUCHER = "voucher"
    TYPE_CHOICES = (
        (TYPE_DISCOUNT, "Discount"),
        (TYPE_VOUCHER, "Voucher"),
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_DISCOUNT,
        blank=True
    )
    # When type == voucher, use this percent to apply across all items
    discount = models.FloatField(default=0.0, blank=True)
    products = models.ManyToManyField(
        Product,
        through='PromotionItem',
        related_name="promotions",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "ecommerce_promotions"
        ordering = ["-created_at"]
