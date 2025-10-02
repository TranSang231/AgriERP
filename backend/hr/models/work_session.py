from base.models import TimeStampedModel
from .office import Office
from common.constants import WorkDay
from django.db import models


class WorkSession(TimeStampedModel):
    start_time = models.TimeField()
    end_time = models.TimeField()
    work_day = models.IntegerField(choices=WorkDay.CHOICES, default=WorkDay.MONDAY, blank=True)
    office = models.ForeignKey(
        Office, related_name="sessions", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "hr_work_sessions"
