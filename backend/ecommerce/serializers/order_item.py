from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Order, Product, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Order.objects.all(),
        source='order'
    )
    product_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Product.objects.all(),
        source='product'
    )
    
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order_id",
            "product_id",
            "product_name",
            "unit",
            "quantity",
            "price",
            "amount",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'product_name': {'required': False},
            'unit': {'required': False},
            'quantity': {'required': False},
            'price': {'required': False},
            'amount': {'required': False}
        }
        read_only_fields = ["id", "amount", "created_at", "updated_at"]