import logging
from django.db import transaction
from rest_framework import serializers
from base.serializers import WritableNestedSerializer

from ..models import GoodsReceipt, GoodsReceiptItem, Product

log = logging.getLogger("ecommerce.goods_receipts")


class GoodsReceiptItemSerializer(WritableNestedSerializer):
    receipt_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        queryset=GoodsReceipt.objects.all(),
        source='receipt',
        write_only=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        required=True,
        allow_null=False,
        queryset=Product.objects.all(),
        source='product'
    )

    class Meta:
        model = GoodsReceiptItem
        fields = [
            "id",
            "receipt_id",
            "product_id",
            "quantity",
            "unit_cost",
            "amount",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "amount", "created_at", "updated_at"]


class GoodsReceiptSerializer(WritableNestedSerializer):
    items = GoodsReceiptItemSerializer(many=True, required=False)

    class Meta:
        model = GoodsReceipt
        fields = [
            "id",
            "supplier_name",
            "reference_code",
            "note",
            "date",
            "is_applied",
            "applied_at",
            "items",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'supplier_name': {'required': False},
            'reference_code': {'required': False},
            'note': {'required': False},
            'date': {'required': False},
        }
        read_only_fields = ["id", "is_applied", "applied_at", "created_at", "updated_at"]
        nested_create_fields = ["items"]
        nested_update_fields = ["items"]
