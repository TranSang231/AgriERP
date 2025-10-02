import datetime

from .base_office import BaseOffice
from .group import Group
from businesses.models import Employee
from django.db import models
from ..managers import OfficeManager


class Office(BaseOffice):
    manager = models.ForeignKey(
        'businesses.Employee', related_name="managed_offices", on_delete=models.SET_NULL, null=True, blank=True
    )
    group = models.ForeignKey(
        Group, related_name="offices", on_delete=models.CASCADE, null=True, blank=True
    )
    remain_leaves_period = models.IntegerField(default=6)

    # detail information
    established_date = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    objects = OfficeManager()

    class Meta:
        db_table = "hr_offices"
