from django.db import models
from django.utils import timezone

from base.models import TimeStampedModel


class TimeRecord(TimeStampedModel):
    """Single work session for an employee from check-in to check-out."""

    employee = models.ForeignKey(
        'businesses.Employee', related_name='time_records', on_delete=models.CASCADE
    )
    office = models.ForeignKey(
        'hr.Office', related_name='time_records', on_delete=models.SET_NULL, null=True, blank=True
    )
    check_in_at = models.DateTimeField()
    check_out_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=32, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'hr_time_records'
        indexes = [
            models.Index(fields=['employee', 'check_in_at']),
            models.Index(fields=['employee', 'check_out_at']),
        ]

    def close(self, check_out_at=None):
        if self.check_out_at:
            return self
        self.check_out_at = check_out_at or timezone.now()
        self.duration_seconds = int((self.check_out_at - self.check_in_at).total_seconds())
        return self



