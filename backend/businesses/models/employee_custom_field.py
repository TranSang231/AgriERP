
from base.models import TimeStampedModel
from common.constants import DataType
from django.db import models
from django.utils import timezone


class EmployeeCustomField(TimeStampedModel):
    name = models.CharField(max_length=80, blank=True)
    data_type = models.CharField(max_length=20, choices=DataType.CHOICES, default=DataType.CHAR_FIELD, blank=True, null=True)
    max_length = models.IntegerField(default=20)

    class Meta:
        db_table = "employee_custom_fields"
