from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from rest_framework.fields import UUIDField
from ..models import Customer, Order
from .order_item import OrderItemSerializer


class OrderSerializer(WritableNestedSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Customer.objects.all(),
        source='customer'
    )
    items = OrderItemSerializer(many=True, required=False)
    
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_id",
            "customer_name",
            "company_name",
            "tax_code",
            "payment_method",
            "payment_status",
            "account_number",
            "vat_rate",
            "shipping_fee",
            "shipping_status",
            "order_status",
            "date",
            "items",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'customer_name': {'required': False},
            'company_name': {'required': False},
            'tax_code': {'required': False},
            'payment_method': {'required': False},
            'payment_status': {'required': False},
            'account_number': {'required': False},
            'vat_rate': {'required': False},
            'shipping_fee': {'required': False},
            'shipping_status': {'required': False},
            'order_status': {'required': False},
            'date': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["items"]
        nested_update_fields = ["items"]