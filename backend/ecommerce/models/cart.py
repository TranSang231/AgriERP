from django.db import models
from django.template.defaultfilters import slugify
from base.models import TimeStampedModel
from .customer import Customer

class Cart(TimeStampedModel):
    customer =  models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        blank=True,
        related_name="cart",
    )

    class Meta:
        db_table = "ecommerce_carts"
        ordering = ["-created_at"]