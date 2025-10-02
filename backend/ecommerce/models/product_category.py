from django.db import models
from base.models import TimeStampedModel
from contents.models import ShortContent

class ProductCategory(TimeStampedModel):
    name = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="product_category_names", null=True, blank=True
    )
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "ecommerce_product_categories"
        ordering = ["-created_at"]
