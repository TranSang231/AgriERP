from base.models import TimeStampedModel
from django.db import models


class BaseOffice(TimeStampedModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
