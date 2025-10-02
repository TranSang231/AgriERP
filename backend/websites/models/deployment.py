# models/article.py
from django.db import models
from base.models import TimeStampedModel
from .site import Site

class Deployment(TimeStampedModel):
    data = models.JSONField(null=True, blank=True)
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.CASCADE, related_name="deployments")

    class Meta:
        db_table = "websites_deployments"
        ordering = ["-created_at"]
