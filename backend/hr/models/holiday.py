from base.models import TimeStampedModel
from django.db import models

from .office import Office


class Holiday(TimeStampedModel):
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    title = models.CharField(max_length=255, null=True)
    descriptions = models.TextField(null=True, blank=True)
    repeat = models.BooleanField(null=False, default=False)
    start_year = models.IntegerField(null=True)
    end_year = models.IntegerField(null=True)
    count = models.IntegerField(null=True, default=0)
    office = models.ForeignKey(Office, related_name="holidays", on_delete=models.CASCADE)

    class Meta:
        db_table = "hr_office_holidays"
