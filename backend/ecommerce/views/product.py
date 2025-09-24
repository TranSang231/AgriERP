from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from common.constants import Http
from base.views import BaseViewSet
from ..models import Product
from ..serializers import ProductSerializer, ProductShortSerializer
from rest_framework.permissions import AllowAny


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
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
        # Allow public access for read-only actions
        if self.action in ["list", "retrieve", "summary_list"]:
            return [AllowAny()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        params = request.query_params

        # Support shop filters without changing frontend
        # search → keyword for BaseViewSet
        if params.get("search"):
            request._request.GET._mutable = True  # type: ignore
            request._request.GET["keyword"] = params.get("search")  # type: ignore

        # category → categories__id exact
        category_id = params.get("category")
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        # min_price / max_price
        min_price = params.get("min_price")
        max_price = params.get("max_price")
        if min_price is not None and min_price != "":
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except Exception:
                pass
        if max_price is not None and max_price != "":
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except Exception:
                pass

        # ordering
        ordering = params.get("ordering")
        if ordering:
            try:
                queryset = queryset.order_by(ordering)
            except Exception:
                pass

        # Let BaseViewSet handle remaining processing (pagination and any extra exact filters)
        self.queryset_map = {"list": queryset}
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=[Http.HTTP_GET], url_path="summary-list")
    def summary_list(self, request, *args, **kwargs):
        queryset, page_size = self.processParams(request);
        if page_size is not None:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)