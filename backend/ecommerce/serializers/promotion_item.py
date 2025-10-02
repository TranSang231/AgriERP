from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Promotion, Product, PromotionItem
from .product_short import ProductShortSerializer

class PromotionItemSerializer(serializers.ModelSerializer):
    promotion_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Promotion.objects.all(),
        source='promotion'
    )
    product = ProductShortSerializer(required=False, read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Product.objects.all(),
        source='product'
    )
    
    class Meta:
        model = PromotionItem
        fields = [
            "id",
            "promotion_id",
            "product",
            "product_id",
            "quantity_limit",
            "quantity_limit_by_customer",
            "discount",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'quantity_limit': {'required': False},
            'quantity_limit_by_customer': {'required': False},
            'discount': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]