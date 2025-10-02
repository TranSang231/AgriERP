from .base_office import BaseOffice
from businesses.models.employee import Employee
from django.db import models
from ..managers import GroupManager


class Group(BaseOffice):
    manager = models.ForeignKey(
        Employee, related_name="managed_groups", on_delete=models.SET_NULL, null=True, blank=True
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="groups"
    )

    objects = GroupManager()

    class Meta:
        db_table = "hr_groups"
