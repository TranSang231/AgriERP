from django.utils.translation import gettext as _
from .base import Const

class WorkDay(Const):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
    CHOICES = (
        (MONDAY, _("Monday")),
        (TUESDAY, _("Tuesday")),
        (WEDNESDAY, _("Wednesday")),
        (THURSDAY, _("Thursday")),
        (FRIDAY, _("Friday")),
        (SATURDAY, _("Saturday")),
        (SUNDAY, _("Sunday")),
    )

    DEFAULT_START_HOUR = "08:00"
    DEFAULT_END_HOUR = "17:30"
    DEFAULT_END_HOUR_MORNING = "12:00"
    DEFAULT_START_HOUR_AFTERNOON = "13:30"
