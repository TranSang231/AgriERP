# models/menu.py
from django.db import models
from base.models import TimeStampedModel
from contents.models.short_content import ShortContent
from ..models import Site


class Menu(TimeStampedModel):
    title = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="site_menu_titles", null=True, blank=True
    )
    url = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    order = models.IntegerField(default=0)
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.CASCADE, related_name="menus")

    def __str__(self):
        return self.title.origin
