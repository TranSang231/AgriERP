from rest_framework import serializers
from ..models import PaymentTransaction, Order


class PaymentTransactionSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        source='order',
        required=True
    )

    class Meta:
        model = PaymentTransaction
        fields = [
            'id',
            'order_id',
            'transaction_type',
            'transaction_status',
            'amount',
            'currency',
            'bank_reference',
            'gateway_transaction_id',
            'gateway_response',
            'notes',
            'processed_at',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'processed_at']
        extra_kwargs = {
            'transaction_type': {'required': False},
            'transaction_status': {'required': False},
            'amount': {'required': False},
            'currency': {'required': False},
            'bank_reference': {'required': False},
            'gateway_transaction_id': {'required': False},
            'gateway_response': {'required': False},
            'notes': {'required': False},
        }

