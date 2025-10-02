from django.db import models
from base.models import TimeStampedModel
from .province import Province
from .delivery_service_provider import DeliveryServiceProvider

class District(TimeStampedModel):
    name = models.CharField(max_length=120, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, related_name="districts")
    mapping = models.ManyToManyField(DeliveryServiceProvider, through='DistrictMapping', blank=True, null=True, related_name="districts")

    class Meta:
        db_table = "ecommerce_districts"

    def __str__(self):
        return self.name