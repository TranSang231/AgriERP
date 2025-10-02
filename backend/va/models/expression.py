from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot 
from . import Intent
# Create your models here.
class Expression(TimeStampedModel):
    text =  models.CharField(max_length=255, blank=True)
    intent = models.ForeignKey(Intent, null=True, blank=True, on_delete=models.CASCADE, related_name="expressions")
    
    def __str__(self):
        return self.text
    
    class Meta:
        db_table = "va_expressions"