from .payment_method import PaymentMethod
from .payment_status import PaymenStatus
from .shipping_status import ShippingStatus
client_constants = {
    "payment_methods": [{"value": x, "description": y} for x, y in PaymentMethod.CHOICES],
    "payment_statuses": [{"value": x, "description": y} for x, y in PaymenStatus.CHOICES],
    "shipping_statuses": [{"value": x, "description": y} for x, y in ShippingStatus.CHOICES]
}