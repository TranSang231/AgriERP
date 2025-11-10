from rest_framework import serializers
from ..models import InventoryConfiguration


class InventoryConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for inventory configuration"""
    
    class Meta:
        model = InventoryConfiguration
        fields = [
            'id',
            'low_stock_threshold_type',
            'low_stock_threshold_value',
            'out_of_stock_threshold',
            'enable_auto_reorder',
            'auto_reorder_quantity_type',
            'auto_reorder_quantity_value',
            'allow_negative_stock',
            'require_transaction_reason',
            'require_transaction_reference',
            'in_stock_label',
            'low_stock_label',
            'out_of_stock_label',
            'auto_reserve_on_order',
            'reservation_expiry_hours',
            'enable_multi_warehouse',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
