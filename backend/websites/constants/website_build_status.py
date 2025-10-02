from django.utils.translation import gettext as _
from common.constants.base import Const

class WebsiteBuildStatus(Const):
     # open > scheduling > in_progress > processed > deployed or failed
    OPEN = 0
    SCHEDULING = 1
    IN_PROGRESS = 2
    PROCESSED = 3
    DEPLOYED = 4
    FAILED = 5
    CHOICES = (
        (OPEN, _("Open")),
        (SCHEDULING, _("Scheduling")),
        (IN_PROGRESS, _("In-progress")),
        (PROCESSED, _("Processed")),
        (DEPLOYED, _("Deployed")),
        (FAILED, _("Failed")),
    )

