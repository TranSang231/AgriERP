from django.utils.translation import gettext as _
from common.constants.base import Const

class AccountStatus(Const):
    # Account status
    DEACTIVE = 0
    ACTIVE = 1
    CHOICES = (
        (DEACTIVE, _("Deactive")),
        (ACTIVE, _("Active"))
    )

