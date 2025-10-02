from django.db import models
from base.models import TimeStampedModel
from .order import Order
from .product import Product


class OrderItem(TimeStampedModel):
    """Data structure for an item in the shopping cart."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, related_name="items")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    # Copy and do not modify these information even the related data change later.
    product_name = models.TextField(max_length=255, blank=True)
    unit = models.TextField(max_length=255, blank=True)
    quantity = models.FloatField(default=0.0, blank=True)
    price = models.FloatField(default=0.0, blank=True)
    amount = models.FloatField(default=0.0, blank=True)

    class Meta:
        db_table = "ecommerce_order_items"

    def save(self, *args, **kwargs):
        if self.price is not None and self.quantity is not None:
            self.amount= self.price * self.quantity
        super().save(*args, **kwargs)
