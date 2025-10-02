from django.db import models
from base.models import TimeStampedModel
from .delivery_service_provider import DeliveryServiceProvider

class Province(TimeStampedModel):
    """Province address, normalize data in our side"""

    name = models.CharField(max_length=120, blank=True)
    mapping = models.ManyToManyField(DeliveryServiceProvider, through='ProvinceMapping', blank=True, null=True, related_name="provinces")

    class Meta:
        db_table = "ecommerce_provinces"

    def __str__(self):
        return self.name