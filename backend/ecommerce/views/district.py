from base.views import BaseViewSet
from ..models import District
from ..serializers import DistrictSerializer

class DistrictViewSet(BaseViewSet):
    queryset = District.objects.all()
    search_map = {
        "name": "icontains"
    }
    serializer_class = DistrictSerializer
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