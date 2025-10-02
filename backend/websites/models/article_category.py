# models/article.py
from django.db import models
from django.template.defaultfilters import slugify
from contents.models import ShortContent
from base.models import TimeStampedModel


class ArticleCategory(TimeStampedModel):
    name = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="article_category_names", null=True, blank=True
    )
    description = models.TextField(null=True, blank=True, default="")
    slug = models.SlugField(max_length=255, blank=True, default="", null=True)

    def __str__(self):
        return self.name.origin

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name.origin)
            
        super().save(*args, **kwargs)

    class Meta:
        db_table = "websites_article_categories"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["slug"])]