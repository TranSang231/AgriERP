from django.db import models
from django.template.defaultfilters import slugify
from base.models import AuditModel
from .namespace import Namespace

class Page(AuditModel):
    title = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, blank=True, default="", null=True)
    content = models.TextField(null=True, blank=True, default="")
    namespace = models.ForeignKey(
        Namespace,on_delete=models.CASCADE,
        blank=True,
        related_name="pages"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:
        db_table = "knowledge_pages"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["slug"])]