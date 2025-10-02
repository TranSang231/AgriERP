from django.utils.translation import gettext as _
from common.constants.base import Const

class RuleStepTypes(Const):
    INTENT = "intent"
    RESPONSE = "response"
    ACTION = "action"
    EVENT = "event"
    CHECKPOINT = "checkpoint"

    CHOICES = (
        (INTENT, _("Intent")),
        (RESPONSE, _("Response")),
        (ACTION, _("Action")),
        (EVENT, _("Event")),
        (CHECKPOINT, _("Checkpoint"))
    )