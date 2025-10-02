
from django.db import models
from base.models import TimeStampedModel
from .employee import Employee
from .employee_custom_field import EmployeeCustomField


class EmployeeAdditionalInformation(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, related_name="additional_information")
    field = models.ForeignKey(EmployeeCustomField, on_delete=models.CASCADE, blank=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "employee_additional_information"
