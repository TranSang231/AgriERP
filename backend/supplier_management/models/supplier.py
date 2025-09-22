from base.models import TimeStampedModel
from django.db import models

class Supplier(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    tax_code = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True) 

    class Meta:
        db_table = "suppliers"
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name