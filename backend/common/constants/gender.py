from django.utils.translation import gettext as _
from .base import Const

class Gender(Const):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    CHOICES = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
        (OTHER, _("Other")),
    )