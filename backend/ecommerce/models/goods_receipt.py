from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal

from base.models import TimeStampedModel
from contents.models import ShortContent
from ..models import Product


class GoodsReceipt(TimeStampedModel):
    supplier_name = models.CharField(max_length=255, blank=True, default='')
    reference_code = models.CharField(max_length=100, blank=True, default='')
    note = models.TextField(blank=True, null=True)
    date = models.DateField(null=True, blank=True)

    # Stock application status
    is_applied = models.BooleanField(default=False, blank=True)
    applied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "ecommerce_goods_receipts"
        ordering = ["-created_at"]

    def mark_applied(self):
        self.is_applied = True
        self.applied_at = timezone.now()
        self.save(update_fields=["is_applied", "applied_at", "updated_at"])


class GoodsReceiptItem(TimeStampedModel):
    receipt = models.ForeignKey(
        GoodsReceipt,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="goods_receipt_items"
    )
    unit = models.ForeignKey(
        ShortContent,
        on_delete=models.SET_NULL,
        related_name="goods_receipt_item_units",
        null=True,
        blank=True
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    class Meta:
        db_table = "ecommerce_goods_receipt_items"

    def save(self, *args, **kwargs):
        # Auto-populate unit from product if not set
        if self.product and not self.unit:
            self.unit = self.product.unit
        # Auto-calculate amount
        self.amount = (self.quantity or Decimal("0.00")) * (self.unit_cost or Decimal("0.00"))
        super().save(*args, **kwargs)
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Tự động tính amount
        self.amount = (self.quantity or Decimal("0.00")) * (self.unit_cost or Decimal("0.00"))
        super().save(*args, **kwargs)
