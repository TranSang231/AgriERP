from django.db import models
from base.models import TimeStampedModel
from .cart import Cart
from .product import Product


class CartItem(TimeStampedModel):
    """Data structure for an item in the shopping cart."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0, blank=True)
    # The origin price is the price when the customer add the product to his cart.
    # We use origin price to tell customer how many the price changed from the time he add it to his cart.
    origin_price = models.FloatField(default=0.0, blank=True)
    selected = models.BooleanField(default=False)

    class Meta:
        db_table = "ecommerce_cart_items"
