from base.views import BaseViewSet
from ..models import ShippingAddress
from ..serializers import ShippingAddressSerializer

class ShippingAddressViewSet(BaseViewSet):
    queryset = ShippingAddress.objects.all()
    search_map = {
        "address": "icontains"
    }
    serializer_class = ShippingAddressSerializer
    required_alternate_scopes = {
        "list": [
            ["ecommerce:addresses:view"],
            ["ecommerce:addresses:edit"],
            ["ecommerce:addresses:view-mine"],
            ["ecommerce:addresses:edit-mine"]
        ],
        "retrieve": [
            ["ecommerce:addresses:view"],
            ["ecommerce:addresses:edit"],
            ["ecommerce:addresses:view-mine"],
            ["ecommerce:addresses:edit-mine"]
        ],
        "create": [["ecommerce:addresses:edit"], ["ecommerce:addresses:edit-mine"]],
        "update": [["ecommerce:addresses:edit"], ["ecommerce:addresses:edit-mine"]],
        "destroy": [["ecommerce:addresses:edit"], ["ecommerce:addresses:edit-mine"]]
    }