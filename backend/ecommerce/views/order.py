from base.views import BaseViewSet
from rest_framework.permissions import AllowAny
from ..models import Order
from ..serializers import OrderSerializer

class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    search_map = {
        "customer_first_name": "icontains",
        "customer_last_name": "icontains"
    }
    serializer_class = OrderSerializer
    # Temporarily allow public access for development
    permission_classes = [AllowAny]
    required_alternate_scopes = {
        "list": [],
        "retrieve": [],
        "create": [],
        "update": [["ecommerce:orders:edit-mine"]],
        "destroy": [["ecommerce:orders:edit-mine"]]
    }