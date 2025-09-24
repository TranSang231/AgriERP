from django.db import models
from base.models import TimeStampedModel
from contents.models import ShortContent, LongContent
from .product_category import ProductCategory

def product_image_path(instance, filename):
    return "/".join(['products', str(instance.id), 'images', filename])

class Product(TimeStampedModel):
    name = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="product_names", null=True, blank=True
    )
    thumbnail = models.ImageField(upload_to=product_image_path, max_length=255, blank=True, null=True)
    description = models.ForeignKey(
        LongContent, on_delete=models.CASCADE, related_name="product_descriptions", null=True, blank=True
    )
    price = models.FloatField(default=0.0, blank=True)
    unit = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="product_units", null=True, blank=True
    )
    # Quantity of goods in stock
    in_stock = models.FloatField(default=0.0, blank=True)
    categories = models.ManyToManyField(
        ProductCategory, related_name="products", null=True, blank=True
    )

    # Packing information
    weight =  models.FloatField(default=0.0, blank=True)
    length =  models.FloatField(default=0.0, blank=True)
    width =  models.FloatField(default=0.0, blank=True)
    height =  models.FloatField(default=0.0, blank=True)

    # Tax information
    tax_rate =  models.FloatField(default=0.0, blank=True)

    class Meta:
        db_table = "ecommerce_products"
        ordering = ["-created_at"]
