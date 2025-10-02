from django.db import models
from base.models import TimeStampedModel
from .product import Product
from django.utils.translation import gettext as _

def product_image_path(instance, filename):
    return "/".join(['products', str(instance.product_id), 'images', str(instance.id), filename])

class ProductImage(TimeStampedModel):
    image = models.ImageField(upload_to=product_image_path, max_length=255, blank=True, null=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="images"
    )

    class Meta:
        db_table = "ecommerce_product_images"