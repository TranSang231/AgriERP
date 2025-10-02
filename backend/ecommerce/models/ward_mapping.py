from django.db import models
from base.models import TimeStampedModel
from .ward import Ward
from .delivery_service_provider import DeliveryServiceProvider


class WardMapping(TimeStampedModel):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, blank=True, related_name="ward_maping")
    delivery_service_provider = models.ForeignKey(DeliveryServiceProvider, on_delete=models.CASCADE, blank=True, related_name="ward_maping")
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "ecommerce_ward_maping"

    def __str__(self):
        return self.name