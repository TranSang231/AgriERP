# models/article.py
from django.db import models
from django.template.defaultfilters import slugify
from common.constants import PublishingStatus
from base.models import TimeStampedModel
from contents.models import ShortContent, LongContent
from .site import Site
from .article_category import ArticleCategory

def article_thumbnail_path(instance, filename):
    return "\\".join(['articles', str(instance.id), 'thumbnails', filename])

class Route(TimeStampedModel):
    path = models.CharField(max_length=255, blank=True)
    title = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="route_titles", null=True, blank=True
    )
    description = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="route_descriptions", null=True, blank=True
    )
    keywords = models.CharField(max_length=250, blank=True)
    content = models.ForeignKey(
        LongContent, on_delete=models.CASCADE, related_name="route_contents", null=True, blank=True
    )
    status = models.SmallIntegerField(choices=PublishingStatus.CHOICES, default=PublishingStatus.DRAFT, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, related_name="routes")

    def __str__(self):
        return self.path

    class Meta:
        db_table = "websites_routes"
        unique_together = [['site', 'path']]
        ordering = ["path"]
        indexes = [models.Index(fields=["path"])]
