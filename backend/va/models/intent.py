from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot
class Intent(TimeStampedModel):
    name =  models.CharField(max_length=255, blank=True)
    bot = models.ForeignKey(Bot, blank=True, on_delete=models.CASCADE, related_name="intents")
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "va_intents"