from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot

class Regex(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    pattern = models.CharField(max_length=255,blank=True, null=True)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.CASCADE, related_name="regexs")
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "va_regexs"