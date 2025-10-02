from django.db import models
from base.models.timestamped import TimeStampedModel


# Create your models here.
class LongContent(TimeStampedModel):
    origin = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "long_contents"

    def __str__(self):
        return self.origin
