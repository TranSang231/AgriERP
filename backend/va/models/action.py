from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot

class Action(TimeStampedModel):
    name =  models.CharField(max_length=255, blank=True)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.CASCADE, related_name="actions")
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "va_actions"