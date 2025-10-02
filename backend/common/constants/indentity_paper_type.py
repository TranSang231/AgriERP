from django.utils.translation import gettext as _
from .base import Const

class IndentityPaperType(Const):
    # Indentity paper types
    CITIZEN_IDENTIFICATION_CARD = "citizen_identification_card"
    IDENTITY_CARD = "identity_card"
    CHOICES = (
        (CITIZEN_IDENTIFICATION_CARD, _("Citizen identification card")),
        (IDENTITY_CARD, _("Identity card")),
    )