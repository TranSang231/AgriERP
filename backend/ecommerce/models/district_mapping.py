from django.db import models
from base.models import TimeStampedModel
from .district import District
from .delivery_service_provider import DeliveryServiceProvider


class DistrictMapping(TimeStampedModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, related_name="district_maping")
    delivery_service_provider = models.ForeignKey(DeliveryServiceProvider, on_delete=models.CASCADE, blank=True, related_name="district_maping")
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "ecommerce_district_maping"

    def __str__(self):
        return self.name