from django.db import models
from common.constants import PublishingStatus
from base.models.timestamped import TimeStampedModel
from contents.models import ShortContent

def website_icon_path(instance, filename):
    return "\\".join(['webstites', str(instance.id), 'images', filename])

def website_template_path(instance, filename):
    return "\\".join(['webstites', str(instance.id), 'templates', filename])

class Site(TimeStampedModel):
    domain_name = models.CharField(max_length=255, unique=True)
    title = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="site_titles", null=True, blank=True
    )
    description = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="site_descriptions", null=True, blank=True
    )
    keywords = models.CharField(max_length=255, null=True, blank=True)
    icon = models.FileField(upload_to=website_icon_path, max_length=255, blank=True, null=True)
    template = models.FileField(upload_to=website_template_path, max_length=255, blank=True, null=True)
    template_settings = models.JSONField(null=True, blank=True)
    status = models.SmallIntegerField(choices=PublishingStatus.CHOICES, default=PublishingStatus.DRAFT, blank=True)

    def __str__(self):
        return self.domain_name
