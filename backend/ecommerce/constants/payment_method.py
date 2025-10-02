from django.utils.translation import gettext as _
from common.constants.base import Const

class PaymentMethod(Const):
    BANK_TRANSFER = 0
    CASH_ON_DELIVERY = 1
    CHOICES = (
        (BANK_TRANSFER, _("Bank transfer")),
        (CASH_ON_DELIVERY, _("Cash on delivery"))
    )

