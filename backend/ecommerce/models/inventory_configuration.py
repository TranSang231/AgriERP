from django.db import models
from base.models import TimeStampedModel


class InventoryConfiguration(TimeStampedModel):
    """
    Configuration for inventory management system
    Allows customization of thresholds and behavior
    """
    
    # Stock Level Thresholds
    low_stock_threshold_type = models.CharField(
        max_length=20,
        choices=[
            ('min_quantity', 'Use Min Quantity'),
            ('percentage', 'Percentage of Max'),
            ('fixed', 'Fixed Value'),
        ],
        default='min_quantity',
        help_text="How to determine low stock threshold"
    )
    low_stock_threshold_value = models.FloatField(
        default=0.0,
        help_text="Value for low stock (e.g., 10 for fixed, 20 for 20%)"
    )
    out_of_stock_threshold = models.FloatField(
        default=0.0,
        help_text="Below this value is considered out of stock"
    )
    
    # Auto-reorder Settings
    enable_auto_reorder = models.BooleanField(
        default=False,
        help_text="Automatically create purchase orders when stock is low"
    )
    auto_reorder_quantity_type = models.CharField(
        max_length=20,
        choices=[
            ('max_quantity', 'Fill to Max Quantity'),
            ('fixed', 'Fixed Reorder Quantity'),
            ('multiple', 'Multiple of Min Quantity'),
        ],
        default='max_quantity',
        help_text="How to calculate reorder quantity"
    )
    auto_reorder_quantity_value = models.FloatField(
        default=0.0,
        help_text="Value for auto reorder calculation"
    )
    
    # Negative Stock Settings
    allow_negative_stock = models.BooleanField(
        default=False,
        help_text="Allow inventory to go below zero (backorder)"
    )
    
    # Stock Movement Settings
    require_transaction_reason = models.BooleanField(
        default=False,
        help_text="Require reason for manual stock adjustments"
    )
    require_transaction_reference = models.BooleanField(
        default=False,
        help_text="Require reference number for stock adjustments"
    )
    
    # Stock Status Labels
    in_stock_label = models.CharField(
        max_length=50,
        default='In Stock',
        help_text="Display label for in-stock items"
    )
    low_stock_label = models.CharField(
        max_length=50,
        default='Low Stock',
        help_text="Display label for low-stock items"
    )
    out_of_stock_label = models.CharField(
        max_length=50,
        default='Out of Stock',
        help_text="Display label for out-of-stock items"
    )
    
    # Reservation Settings
    auto_reserve_on_order = models.BooleanField(
        default=True,
        help_text="Automatically reserve stock when order is placed"
    )
    reservation_expiry_hours = models.IntegerField(
        default=24,
        help_text="Hours before unreleased reservations expire"
    )
    
    # Multi-warehouse Settings
    enable_multi_warehouse = models.BooleanField(
        default=False,
        help_text="Enable multi-warehouse inventory tracking"
    )
    
    # Singleton pattern - only one configuration should exist
    is_active = models.BooleanField(
        default=True,
        help_text="Only one configuration can be active"
    )
    
    class Meta:
        db_table = "ecommerce_inventory_configuration"
        verbose_name = "Inventory Configuration"
        verbose_name_plural = "Inventory Configurations"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Inventory Config (Active: {self.is_active})"
    
    def save(self, *args, **kwargs):
        """Ensure only one active configuration exists"""
        if self.is_active:
            # Deactivate all other configurations
            InventoryConfiguration.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_config(cls):
        """Get the active configuration, or create default if none exists"""
        config = cls.objects.filter(is_active=True).first()
        if not config:
            config = cls.objects.create(is_active=True)
        return config
    
    def get_low_stock_threshold(self, inventory):
        """
        Calculate low stock threshold for a given inventory item
        
        Args:
            inventory: Inventory instance
            
        Returns:
            float: The threshold value
        """
        if self.low_stock_threshold_type == 'min_quantity':
            return inventory.min_quantity
        elif self.low_stock_threshold_type == 'percentage':
            if inventory.max_quantity:
                return inventory.max_quantity * (self.low_stock_threshold_value / 100)
            return inventory.min_quantity
        elif self.low_stock_threshold_type == 'fixed':
            return self.low_stock_threshold_value
        return inventory.min_quantity
    
    def is_low_stock(self, inventory):
        """Check if inventory is low stock based on configuration"""
        threshold = self.get_low_stock_threshold(inventory)
        return (inventory.current_quantity > self.out_of_stock_threshold and 
                inventory.current_quantity <= threshold)
    
    def is_out_of_stock(self, inventory):
        """Check if inventory is out of stock based on configuration"""
        return inventory.current_quantity <= self.out_of_stock_threshold
    
    def is_in_stock(self, inventory):
        """Check if inventory is in stock based on configuration"""
        threshold = self.get_low_stock_threshold(inventory)
        return inventory.current_quantity > threshold
    
    def calculate_reorder_quantity(self, inventory):
        """
        Calculate how much to reorder for low stock inventory
        
        Args:
            inventory: Inventory instance
            
        Returns:
            float: Quantity to reorder
        """
        if not self.enable_auto_reorder:
            return 0
        
        if self.auto_reorder_quantity_type == 'max_quantity':
            if inventory.max_quantity:
                return max(0, inventory.max_quantity - inventory.current_quantity)
            return inventory.min_quantity * 2  # Fallback: 2x min
        elif self.auto_reorder_quantity_type == 'fixed':
            return self.auto_reorder_quantity_value
        elif self.auto_reorder_quantity_type == 'multiple':
            return inventory.min_quantity * self.auto_reorder_quantity_value
        
        return 0
