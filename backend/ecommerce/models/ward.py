from django.db import models
from base.models import TimeStampedModel
from .district import District
from .delivery_service_provider import DeliveryServiceProvider

class Ward(TimeStampedModel):
    """Ward address, normalize data in our side"""

    name = models.CharField(max_length=120, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, related_name="wards")
    mapping = models.ManyToManyField(DeliveryServiceProvider, through='WardMapping', blank=True, null=True, related_name="wards")


    class Meta:
        db_table = "ecommerce_wards"

    def __str__(self):
        return self.name