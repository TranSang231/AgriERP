from django.db import models
from base.models import TimeStampedModel
class UnitType(TimeStampedModel):
    name = models.CharField(max_length=255, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    class Meta:
        db_table = "hr_organization_unit_types"
