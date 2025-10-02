import datetime

from django.db import models
from .group_concat import GroupConcat


class GroupManager(models.Manager):

    def with_short_info(self):
        return self.annotate(
            manager_title=GroupConcat("manager__titles__title", separator=", ")
        )
