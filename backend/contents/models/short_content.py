from django.db import models
from base.models.timestamped import TimeStampedModel


# Create your models here.
class ShortContent(TimeStampedModel):
    origin = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        db_table = "short_contents"

    def __str__(self):
        return self.origin
