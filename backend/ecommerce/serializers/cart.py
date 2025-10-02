from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Customer, Cart
from .cart_item import CartItemSerializer

class CartSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Customer.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='customer'
    )
    items = CartItemSerializer(many=True, required=False)
    
    class Meta:
        model = Cart
        fields = [
            "id",
            "customer_id",
            "items",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]