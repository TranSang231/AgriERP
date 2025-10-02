from django.db import models
from base.models.timestamped import TimeStampedModel
from .synonym import Synonym

class SynonymVariant(TimeStampedModel):
    value =  models.CharField(max_length=255, blank=True)
    synonym = models.ForeignKey(Synonym, blank=True, on_delete=models.CASCADE, related_name="variants")
    
    def __str__(self):
        return self.value
    
    class Meta:
        db_table = "va_synonym_variants"