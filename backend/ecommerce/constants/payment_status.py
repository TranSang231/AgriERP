from django.utils.translation import gettext as _
from common.constants.base import Const

class PaymenStatus(Const):
    #The payment process has begun, but it's not yet final.
    INITIATED = 0
    # The payment is being processed and is awaiting approval or completion. 
    PENDING = 1
    # The payment has been approved by the payment provider, but the funds haven't been captured yet. 
    AUTHORIZED = 2
    # The payment has been successfully captured, and the funds have been transferred to the merchant's account. 
    CAPTURED = 3
    # The payment process has finished, and the transaction is fully settled. 
    COMPLETED = 4
    # The payment was rejected by the payment provider.
    REFUSED_OR_DECLINED = 5
    # An unexpected error occurred during the payment process.
    ERROR = 6
    # The payment was canceled before it was completed.
    CANCELED = 7
    # The payment has been processed and the funds have been moved to the recipient's account.
    SETTLED = 8
    CHOICES = (
        (INITIATED, _("Initiated")),
        (PENDING, _("Pending")),
        (AUTHORIZED, _("Authorized")),
        (CAPTURED, _("Captured")),
        (COMPLETED, _("Completed")),
        (REFUSED_OR_DECLINED, _("Refused/Declined")),
        (ERROR, _("Error")),
        (CANCELED, _("Canceled")),
        (SETTLED, _("Settled"))
    )

