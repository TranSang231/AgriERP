from django.db import models
from base.models.timestamped import TimeStampedModel
from ..constants import RuleStepTypes
from .rule import Rule

class RuleStep(TimeStampedModel):
    order = models.IntegerField(default=0, null=True, blank=True)
    rule = models.ForeignKey(Rule, null=True, blank=True, on_delete=models.CASCADE, related_name="steps")
    type = models.CharField(choices=RuleStepTypes.CHOICES,max_length=80, blank=True)
    payload =  models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = "va_rule_steps"