from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from common.constants import Http
from base.views import BaseViewSet
from ..models import Product
from ..serializers import ProductSerializer, ProductShortSerializer


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.select_related('inventory').all()
    search_map = {
        "name__origin": "icontains",
        "description__origin": "icontains"
    }
    serializer_class = ProductSerializer
    serializer_map = {
        "summary_list": ProductShortSerializer,
    }
    required_alternate_scopes = {
        "list": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "retrieve": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "create": [["ecommerce:products:edit"]],
        "update": [["ecommerce:products:edit"]],
        "destroy": [["ecommerce:products:edit"]],
        "summary_list": [["ecommerce:products:view"], ["ecommerce:products:edit"]]
    }

    def get_permissions(self):
        """Allow public access for listing and viewing products."""
        if self.action in ["list", "retrieve", "summary_list"]:
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=[Http.HTTP_GET], url_path="summary-list")
    def summary_list(self, request, *args, **kwargs):
        queryset, page_size = self.processParams(request)
        if page_size is not None:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)