from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot

class Conversation(TimeStampedModel):
    conversation = models.TextField(blank=True, null=True)
    story = models.TextField(blank=True, null=True)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.CASCADE, related_name="conversations")
    def __str__(self):
        return self.action_name
    
    class Meta:
        db_table = "va_conversations"