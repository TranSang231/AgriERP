from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot
from ..constants import NLUDataTypes
class Entity(TimeStampedModel):
    name =  models.CharField(max_length=255, blank=True)
    slot_data_type =  models.CharField(choices=NLUDataTypes.CHOICES,max_length=255 ,blank=True, null=True)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.CASCADE, related_name="entities")
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "va_entities"