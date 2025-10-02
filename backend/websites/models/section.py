# models/article.py
from django.db import models
from base.models import TimeStampedModel
from .site import Site
from .article import Article

class Section(TimeStampedModel):
    name = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    articles = models.ManyToManyField(Article, through='SectionArticle', blank=True, null=True, related_name="sections")
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.CASCADE, related_name="sections")

    class Meta:
        db_table = "websites_sections"
        unique_together = [["site", "name"]]
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]
