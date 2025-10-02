from django.db import models
from base.models.timestamped import TimeStampedModel
from common.constants import Language
from .long_content import LongContent


# Create your models here.
class LongTranslate(TimeStampedModel):
    content = models.ForeignKey(                        
        LongContent,
        related_name="translates",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    language = models.CharField(max_length=5, choices=Language.CHOICES, default=Language.EN)
    value = models.TextField(null=True)

    class Meta:
        db_table = "long_translates"
        unique_together=[['content', 'language']]

    def __str__(self):
        return self.value
