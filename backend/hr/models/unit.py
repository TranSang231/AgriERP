from django.db import models
from base.models import TimeStampedModel
from .unit_type import UnitType  
class Unit(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    slack_channel = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(
        UnitType, related_name="units", on_delete=models.SET_NULL, blank=True, null=True
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="units"
    )
    manager = models.ForeignKey(
        'businesses.Employee', related_name="managed_units", on_delete=models.SET_NULL, blank=True, null=True
    )
    members = models.ManyToManyField('businesses.Employee', through='UnitMember', blank=True, null=True, related_name="units")
    
    class Meta:
        db_table = "hr_organization_units"
