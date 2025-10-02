from django.db import models
from django.template.defaultfilters import slugify
from base.models import TimeStampedModel
from ..constants import PaymentMethod, PaymenStatus, ShippingStatus, OrderStatus
from .customer import Customer


class Order(TimeStampedModel):
    customer =  models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="orders",
    )
    customer_name = models.CharField(max_length=200, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    tax_code = models.CharField(max_length=15, blank=True)
    payment_method = models.SmallIntegerField(choices=PaymentMethod.CHOICES, default=PaymentMethod.CASH_ON_DELIVERY, blank=True)
    payment_status = models.SmallIntegerField(choices=PaymenStatus.CHOICES, default=PaymenStatus.INITIATED, blank=True)
    account_number = models.CharField(max_length=15, blank=True)
    vat_rate = models.FloatField(default=0.0, blank=True)
    shipping_fee = models.FloatField(default=0.0, blank=True)
    shipping_status = models.SmallIntegerField(choices=ShippingStatus.CHOICES, default=ShippingStatus.BOOKED, blank=True)
    order_status = models.SmallIntegerField(choices=OrderStatus.CHOICES, default=OrderStatus.NEW, blank=True)

    date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "ecommerce_orders"
        ordering = ["-created_at"]