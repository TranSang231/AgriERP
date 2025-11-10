from django.db import models
from django.conf import settings
from base.models import TimeStampedModel
from .product import Product


class Inventory(TimeStampedModel):
    """
    Inventory model to track product stock levels
    """
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory"
    )
    current_quantity = models.FloatField(default=0.0, help_text="Current stock quantity")
    min_quantity = models.FloatField(default=0.0, help_text="Minimum stock level")
    max_quantity = models.FloatField(null=True, blank=True, help_text="Maximum stock level")
    reserved_quantity = models.FloatField(default=0.0, help_text="Reserved quantity for orders")
    
    class Meta:
        db_table = "ecommerce_inventory"
        ordering = ["-updated_at"]
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    def __str__(self):
        """Safe string representation that handles deleted products"""
        try:
            if self.product:
                return f"Inventory for {self.product}"
        except Exception:
            pass
        return f"Inventory ID {self.id}"

    @property
    def available_quantity(self):
        """Available quantity for sale (current - reserved)"""
        try:
            return max(0, self.current_quantity - self.reserved_quantity)
        except Exception:
            return 0

    @property
    def is_low_stock(self):
        """Check if stock is below minimum level"""
        try:
            return self.current_quantity <= self.min_quantity
        except Exception:
            return False

    @property
    def is_out_of_stock(self):
        """Check if product is out of stock"""
        try:
            return self.current_quantity <= 0
        except Exception:
            return True


class InventoryTransaction(TimeStampedModel):
    """
    Track inventory movements (in/out adjustments)
    """
    TRANSACTION_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjust', 'Adjustment'),
        ('reserve', 'Reserve'),
        ('unreserve', 'Unreserve'),
    ]
    
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.FloatField(help_text="Quantity change (positive for in, negative for out)")
    reference_number = models.CharField(max_length=100, blank=True, help_text="Reference number (order, receipt, etc.)")
    reason = models.TextField(blank=True, help_text="Reason for transaction")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventory_transactions"
    )
    
    class Meta:
        db_table = "ecommerce_inventory_transactions"
        ordering = ["-created_at"]
        verbose_name = "Inventory Transaction"
        verbose_name_plural = "Inventory Transactions"

    def __str__(self):
        """Safe string representation that handles deleted products"""
        try:
            if self.inventory and self.inventory.product:
                return f"{self.transaction_type} - {self.quantity} - {self.inventory.product}"
            elif self.inventory:
                return f"{self.transaction_type} - {self.quantity} - Inventory ID {self.inventory.id}"
        except Exception:
            pass
        return f"{self.transaction_type} - {self.quantity} - Transaction ID {self.id}"
