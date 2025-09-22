from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Supplier

from base.views import BaseViewSet
from common.constants import Http
from ..serializers import SupplierSerializer

class SupplierViewSet(BaseViewSet):
    queryset = Supplier.objects.filter(is_active=True).order_by("-updated_at")
    serializer_class = SupplierSerializer

    search_map = {
        "name": "icontains",
        "email": "icontains",
        "phone": "icontains",
        "tax_code": "icontains",
    }

    required_alternate_scopes = {
        "list": [["suppliers:view"]],
        "retrieve": [["suppliers:view"]],
        "create": [["suppliers:edit"]],
        "update": [["suppliers:edit"]],
        "partial_update": [["suppliers:edit"]],
        "destroy": [["suppliers:edit"]],
        "restore": [["suppliers:edit"]],
    }

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active"])
        self.clear_querysets_cache()
        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=[Http.HTTP_GET], url_path="all")
    def all(self, request, *args, **kwargs):
        include_inactive = request.query_params.get("include_inactive", "false").lower() == "true"
        qs = Supplier.objects.all() if include_inactive else Supplier.objects.filter(is_active=True)
        page =self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)