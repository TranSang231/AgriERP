from django.utils.translation import gettext as _
from .base import Const

class PaperValidateStatus(Const):
    WAITING_FOR_CONFIRM = 0
    CONFIRMING = 1
    FINE = 2
    INVALID = 3
    CHOICES = (
        (WAITING_FOR_CONFIRM, _("Waiting for comfim")),
        (CONFIRMING, _("Confirming")),
        (FINE, _("The information and papers are fine")),
        (INVALID, _("The information or papers is not correct"))
    )

