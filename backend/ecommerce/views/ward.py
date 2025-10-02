from base.views import BaseViewSet
from ..models import Ward
from ..serializers import WardSerializer

class WardViewSet(BaseViewSet):
    queryset = Ward.objects.all()
    search_map = {
        "name": "icontains"
    }
    serializer_class = WardSerializer
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
        "create": [["ecommerce:addresses:edit"]],
        "update": [["ecommerce:addresses:edit"]],
        "destroy": [["ecommerce:addresses:edit"]]
    }