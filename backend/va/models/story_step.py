from django.db import models
from base.models.timestamped import TimeStampedModel
from ..constants import StoryStepTypes
from .story import Story

class StoryStep(TimeStampedModel):
    order = models.IntegerField(default=0, null=True, blank=True)
    story = models.ForeignKey(Story, null=True, blank=True, on_delete=models.CASCADE, related_name="steps")
    type = models.CharField(choices=StoryStepTypes.CHOICES,max_length=80, blank=True)
    payload =  models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = "va_story_steps"