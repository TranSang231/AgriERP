from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot
from .intent import Intent
from .entity import Entity
class Utterance(TimeStampedModel):
    text =  models.CharField(max_length=255, blank=True)
    bot = models.ForeignKey(
        Bot,
        blank=True,
        on_delete=models.CASCADE,
        related_name="utterances"
    )
    intent = models.ForeignKey(
        Intent,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="utterances"
    )
    entities = models.ManyToManyField(
        Entity,
        through='UtteranceEntity',
        related_name="utterances",
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "va_utterances"