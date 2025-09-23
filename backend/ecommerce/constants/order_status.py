from django.utils.translation import gettext as _
from common.constants.base import Const


class OrderStatus(Const):
    NEW = 0
    CONFIRMED = 1
    PACKING = 2
    SHIPPED = 3
    COMPLETED = 4
    CANCELLED = 5

    CHOICES = (
        (NEW, _("New")),
        (CONFIRMED, _("Confirmed")),
        (PACKING, _("Packing")),
        (SHIPPED, _("Shipped")),
        (COMPLETED, _("Completed")),
        (CANCELLED, _("Cancelled"))
    ) 