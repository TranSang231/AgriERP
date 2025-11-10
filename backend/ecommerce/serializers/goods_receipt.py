import logging
from django.db import transaction
from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from contents.serializers import ShortContentSerializer
from contents.models import ShortContent

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
    unit_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        queryset=ShortContent.objects.all(),
        source='unit',
        write_only=True
    )
    unit = ShortContentSerializer(read_only=True)
    
    # Add product details for display
    product_name = serializers.SerializerMethodField()
    product_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = GoodsReceiptItem
        fields = [
            "id",
            "receipt_id",
            "product_id",
            "product_name",
            "product_thumbnail",
            "unit_id",
            "unit",
            "quantity",
            "unit_cost",
            "amount",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "amount", "created_at", "updated_at"]
    
    def get_product_name(self, obj):
        if obj.product and obj.product.name:
            return obj.product.name.origin
        return None
    
    def get_product_thumbnail(self, obj):
        if obj.product and obj.product.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.thumbnail.url)
        return None


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
            'supplier_name': {'required': False, 'allow_blank': True},
            'reference_code': {'required': False, 'allow_blank': True},
            'note': {'required': False, 'allow_blank': True, 'allow_null': True},
            'date': {'required': False, 'allow_null': True},
        }
        read_only_fields = ["id", "is_applied", "applied_at", "created_at", "updated_at"]
        nested_create_fields = ["items"]
        nested_update_fields = ["items"]
