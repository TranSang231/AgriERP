from django.utils.translation import gettext as _
from common.constants.base import Const

class LeavePaidType(Const):
    INSURANCE_PAID = "insurance_paid"
    COMPANY_PAID = "company_paid"
    NONE_PAID = "none_paid"
    CHOICES = (
        (INSURANCE_PAID, _("Insurance paid")),
        (COMPANY_PAID, _("Company paid")),
        (NONE_PAID, _("None paid"))
    )