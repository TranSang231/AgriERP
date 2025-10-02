from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot
from .regex import Regex

class Synonym(TimeStampedModel):
    reference =  models.CharField(max_length=255, blank=True)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.CASCADE, related_name="synonyms")
    def __str__(self):
        return self.synonym_reference
    
    class Meta:
        db_table = "va_synonyms"