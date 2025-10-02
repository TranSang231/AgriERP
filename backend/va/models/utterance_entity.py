from django.db import models
from base.models.timestamped import TimeStampedModel
from .utterance import Utterance
from .entity import Entity
class UtteranceEntity(TimeStampedModel):
    utterance = models.ForeignKey(
        Utterance,
        blank=True,
        on_delete=models.CASCADE,
        related_name="utterance_entities")
    entity = models.ForeignKey(
        Entity,
        blank=True,
        on_delete=models.CASCADE,
        related_name="utterance_entities")
    text =  models.CharField(max_length=255, blank=True, null=True)
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)
    style =  models.CharField(max_length=256, blank=True, null=True)
    
    class Meta:
        db_table = "va_intents_utterance_entities"