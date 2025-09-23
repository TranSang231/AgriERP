import logging
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from base.views import BaseViewSet
from common.constants import Http
from ..models import GoodsReceipt, Product
from ..serializers import GoodsReceiptSerializer


log = logging.getLogger("ecommerce.goods_receipts")


class GoodsReceiptViewSet(BaseViewSet):
    queryset = GoodsReceipt.objects.all()
    search_map = {
        "supplier_name": "icontains",
        "reference_code": "icontains",
        "note": "icontains",
    }
    serializer_class = GoodsReceiptSerializer
    required_alternate_scopes = {
        "list": [
            ["ecommerce:goods-receipts:view"],
            ["ecommerce:goods-receipts:edit"],
            ["ecommerce:orders:view"],
            ["ecommerce:orders:edit"],
        ],
        "retrieve": [
            ["ecommerce:goods-receipts:view"],
            ["ecommerce:goods-receipts:edit"],
            ["ecommerce:orders:view"],
            ["ecommerce:orders:edit"],
        ],
        "create": [["ecommerce:goods-receipts:edit"], ["ecommerce:orders:edit"]],
        "update": [["ecommerce:goods-receipts:edit"], ["ecommerce:orders:edit"]],
        "destroy": [["ecommerce:goods-receipts:edit"], ["ecommerce:orders:edit"]],
        "apply": [["ecommerce:goods-receipts:edit"], ["ecommerce:orders:edit"]],
    }

    def create(self, request, *args, **kwargs):
        try:
            log.debug("[GoodsReceipt.create] payload=%s", request.data)
        except Exception:
            pass
        response = super().create(request, *args, **kwargs)
        try:
            log.debug("[GoodsReceipt.create] response=%s", getattr(response, 'data', None))
        except Exception:
            pass
        return response

    def update(self, request, *args, **kwargs):
        try:
            log.debug("[GoodsReceipt.update] id=%s payload=%s", kwargs.get('pk'), request.data)
        except Exception:
            pass
        response = super().update(request, *args, **kwargs)
        try:
            log.debug("[GoodsReceipt.update] id=%s response=%s", kwargs.get('pk'), getattr(response, 'data', None))
        except Exception:
            pass
        return response

    @action(detail=True, methods=[Http.HTTP_POST], url_path="apply")
    def apply(self, request, *args, **kwargs):
        receipt: GoodsReceipt = self.get_object()
        if receipt.is_applied:
            return Response({"detail": "Receipt already applied"}, status=status.HTTP_400_BAD_REQUEST)

        items = receipt.items.select_related("product").all()
        for item in items:
            product: Product = item.product
            product.in_stock = (product.in_stock or 0.0) + (item.quantity or 0.0)
            product.save(update_fields=["in_stock", "updated_at"])

        receipt.mark_applied()

        serializer = self.get_serializer(receipt)
        return Response(serializer.data, status=status.HTTP_200_OK)


