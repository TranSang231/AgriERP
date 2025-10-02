from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot

class Rule(TimeStampedModel):
    name =  models.CharField(max_length=255, blank=True)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.CASCADE, related_name="rules")
    conversation_start = models.BooleanField(blank=True, default=False)
    wait_for_user_input = models.BooleanField(blank=True, default=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "va_rules"