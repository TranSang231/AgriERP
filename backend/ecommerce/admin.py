from django.contrib import admin
from .models import InventoryConfiguration, Inventory, InventoryTransaction


@admin.register(InventoryConfiguration)
class InventoryConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for Inventory Configuration"""
    list_display = [
        'id',
        'is_active',
        'low_stock_threshold_type',
        'out_of_stock_threshold',
        'enable_auto_reorder',
        'allow_negative_stock',
        'created_at',
    ]
    list_filter = ['is_active', 'enable_auto_reorder', 'allow_negative_stock']
    search_fields = ['id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Stock Level Thresholds', {
            'fields': (
                'low_stock_threshold_type',
                'low_stock_threshold_value',
                'out_of_stock_threshold',
            )
        }),
        ('Auto Reorder Settings', {
            'fields': (
                'enable_auto_reorder',
                'auto_reorder_quantity_type',
                'auto_reorder_quantity_value',
            )
        }),
        ('Stock Movement Settings', {
            'fields': (
                'allow_negative_stock',
                'require_transaction_reason',
                'require_transaction_reference',
            )
        }),
        ('Display Labels', {
            'fields': (
                'in_stock_label',
                'low_stock_label',
                'out_of_stock_label',
            )
        }),
        ('Reservation Settings', {
            'fields': (
                'auto_reserve_on_order',
                'reservation_expiry_hours',
            )
        }),
        ('Advanced', {
            'fields': (
                'enable_multi_warehouse',
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    """Admin interface for Inventory"""
    list_display = [
        'id',
        'product',
        'current_quantity',
        'min_quantity',
        'max_quantity',
        'reserved_quantity',
        'is_low_stock',
        'is_out_of_stock',
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['product__name']
    readonly_fields = ['created_at', 'updated_at', 'available_quantity', 'is_low_stock', 'is_out_of_stock']


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    """Admin interface for Inventory Transactions"""
    list_display = [
        'id',
        'inventory',
        'transaction_type',
        'quantity',
        'reference_number',
        'created_at',
    ]
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['reference_number', 'inventory__product__name']
    readonly_fields = ['created_at', 'updated_at']
