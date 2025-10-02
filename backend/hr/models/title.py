from django.db import models
from base.models import TimeStampedModel
from businesses.models import Employee


class Title(TimeStampedModel):
    title = models.CharField(max_length=80, unique=True)
    employees = models.ManyToManyField(Employee, related_name="titles", null=True, blank=True)

    class Meta:
        db_table = "hr_titles"

    def __repr__(self):
        return self.title
