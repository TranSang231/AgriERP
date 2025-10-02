from django.db import models
from django.template.defaultfilters import slugify
from base.models import AuditModel
from .namespace import Namespace

class HomePage(AuditModel):
    content = models.TextField(null=True, blank=True, default="")
    namespace =  models.OneToOneField(
        Namespace,
        on_delete=models.CASCADE,
        blank=True,
        related_name="home_page",
    )

    class Meta:
        db_table = "knowledge_home_pages"
        ordering = ["-created_at"]