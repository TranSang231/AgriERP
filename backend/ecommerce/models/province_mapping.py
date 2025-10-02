from django.db import models
from base.models import TimeStampedModel
from .province import Province
from .delivery_service_provider import DeliveryServiceProvider


class ProvinceMapping(TimeStampedModel):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, related_name="maping")
    delivery_service_provider = models.ForeignKey(DeliveryServiceProvider, on_delete=models.CASCADE, blank=True, related_name="province_maping")
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "ecommerce_province_maping"

    def __str__(self):
        return self.name