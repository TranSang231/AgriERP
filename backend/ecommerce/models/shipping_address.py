from django.db import models
from base.models import TimeStampedModel
from .province import Province
from .district import District
from .ward import Ward
from .customer import Customer

class ShippingAddress(TimeStampedModel):
    """Customer address for shipping"""

    customer = models.ForeignKey(Customer, related_name="shipping_addresses", on_delete=models.SET_NULL, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_addresses")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_addresses")
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_addresses")
    address = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        db_table = "ecommerce_shipping_addresses"

    def __str__(self):
        return self.address