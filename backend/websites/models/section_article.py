from base.models import TimeStampedModel
from .section import Section
from .article import Article
from django.db import models


class SectionArticle(TimeStampedModel):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        db_table = "websites_section_acticles"
