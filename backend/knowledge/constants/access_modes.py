from django.utils.translation import gettext as _
from common.constants.base import Const

class AccessMode(Const):
    PRIVATE = 0
    INTERNAL =1
    PUBLIC = 2
    CHOICES = (
        (PRIVATE, _("Private")),
        (INTERNAL, _("Internal")),
        (PUBLIC, _("Public"))
    )

