from django.db import models
from base.models import TimeStampedModel
from businesses.models.employee import Employee
from .unit import Unit
class UnitMember(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    class Meta:
        db_table = "hr_organization_unit_members"
