from django.db import models
from base.models import TimeStampedModel


class DeliveryServiceProvider(TimeStampedModel):
    name = models.CharField(max_length=120, blank=True)
    config = models.JSONField(null=True, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "ecommerce_delivery_service_providers"

    def __str__(self):
        return self.name