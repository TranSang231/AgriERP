from django.db import models
from base.models.timestamped import TimeStampedModel
from .short_content import ShortContent
from common.constants import Language

# Create your models here.
class ShortTranslate(TimeStampedModel):
    content = models.ForeignKey(
        ShortContent,
        related_name="translates",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    language = models.CharField(max_length=5,choices=Language.CHOICES, default=Language.EN)
    value = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "short_translates"
        unique_together = [['content', 'language']]

    def __str__(self):
        return self.value
