from django.utils.translation import gettext as _
from .base import Const

class PublishingStatus(Const):
    DRAFT = 0
    PUBLISHED =1
    UN_PUBLISHED = 2
    CHOICES = (
        (DRAFT, _("Draft")),
        (PUBLISHED, _("Published")),
        (UN_PUBLISHED, _("Un-published"))
    )

