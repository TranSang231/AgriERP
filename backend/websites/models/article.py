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

class Article(TimeStampedModel):
    title = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="article_titles", null=True, blank=True
    )
    slug = models.SlugField(max_length=250, blank=True, default="")
    categories = models.ManyToManyField(
        ArticleCategory, related_name="articles", null=True, blank=True
    )
    description = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="article_descriptions", null=True, blank=True
    )
    keywords = models.CharField(max_length=250, blank=True)
    thumbnail = models.ImageField(upload_to=article_thumbnail_path, max_length=255, blank=True, null=True)
    content = models.ForeignKey(
        LongContent, on_delete=models.CASCADE, related_name="article_contents", null=True, blank=True
    )
    status = models.SmallIntegerField(choices=PublishingStatus.CHOICES, default=PublishingStatus.DRAFT, blank=True)
    sites = models.ManyToManyField(
        Site, related_name="articles", null=True, blank=True
    )

    def __str__(self):
        return self.title.origin

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title.origin)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "websites_articles"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["slug"])]
