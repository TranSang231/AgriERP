from django.utils.translation import gettext as _
from common.constants.base import Const

class EvaluationTemplateStatus(Const):
    DRAF = 0
    ACTIVATED = 1
    DEACTIVATED = 2
    CHOICES = (
        (DRAF, _("Draft")),
        (ACTIVATED, _("Activated")),
        (DEACTIVATED, _("Deactivated"))
    )
