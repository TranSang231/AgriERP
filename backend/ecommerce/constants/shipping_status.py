from django.utils.translation import gettext as _
from common.constants.base import Const

class ShippingStatus(Const):
    BOOKED = 0
    PACKING = 1
    DELIVERING = 2
    DELIVERED = 3
    RETURN_REQUESTED = 4
    RETURNING = 5
    RETURED = 6
    CHOICES = (
        (BOOKED, _("Booked")),
        (PACKING, _("Packing")),
        (DELIVERING, _("Delivering")),
        (DELIVERED, _("Delivered")),
        (RETURN_REQUESTED, _("Return requested")),
        (RETURNING, _("Returning")),
        (RETURED, _("Returned"))
    )

