from django.db import models
from base.models.timestamped import TimeStampedModel
from common.constants import Language

class Bot(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True)
    config = models.JSONField(null=True, blank=True)
    output_folder = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "va_bots"