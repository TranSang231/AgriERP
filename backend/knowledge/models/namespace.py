from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from base.models import TimeStampedModel
from businesses.models import Employee
from ..constants import AccessMode

def logo_path(instance, filename):
    return  "\\".join(['knowledge', 'namespaces', str(instance.id), 'logos', filename])

class Namespace(TimeStampedModel):
    name = models.TextField(null=True, blank=True, default="")
    slug = models.SlugField(max_length=255, blank=True, default="", null=True)
    logo = models.ImageField(upload_to=logo_path, max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True, default="")
    access = models.SmallIntegerField(choices=AccessMode.CHOICES, default=AccessMode.PRIVATE, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owner_namespaces",
    )
    members = models.ManyToManyField(Employee, through='NamespaceMember', blank=True, null=True, related_name="namespaces")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        db_table = "knowledge_namespaces"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["slug"])]