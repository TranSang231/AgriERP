from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Cart, Product, CartItem
from .product import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    cart_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Cart.objects.all(),
        source='cart'
    )
    product = ProductSerializer(required=False)
    product_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Product.objects.all(),
        source='product'
    )
    
    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart_id",
            "product",
            "product_id",
            "quantity",
            "origin_price",
            "selected",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'quantity': {'required': False},
            'origin_price': {'required': False},
            'selected': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]