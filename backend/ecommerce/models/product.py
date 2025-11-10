from django.db import models
from base.models import TimeStampedModel
from contents.models import ShortContent, LongContent
from .product_category import ProductCategory

def product_image_path(instance, filename):
    return "/".join(['products', str(instance.id), 'images', filename])

class Product(TimeStampedModel):
    name = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="product_names", null=True, blank=True
    )
    thumbnail = models.ImageField(upload_to=product_image_path, max_length=255, blank=True, null=True)
    description = models.ForeignKey(
        LongContent, on_delete=models.CASCADE, related_name="product_descriptions", null=True, blank=True
    )
    price = models.FloatField(default=0.0, blank=True)
    unit = models.ForeignKey(
        ShortContent, on_delete=models.CASCADE, related_name="product_units", null=True, blank=True
    )
    # ❌ REMOVED: in_stock field - now using @property that reads from Inventory
    # Stock quantity is now managed exclusively in Inventory model (Single Source of Truth)
    categories = models.ManyToManyField(
        ProductCategory, related_name="products", null=True, blank=True
    )

    # Packing information
    weight =  models.FloatField(default=0.0, blank=True)
    length =  models.FloatField(default=0.0, blank=True)
    width =  models.FloatField(default=0.0, blank=True)
    height =  models.FloatField(default=0.0, blank=True)

    # Tax information
    tax_rate =  models.FloatField(default=0.0, blank=True)

    class Meta:
        db_table = "ecommerce_products"
        ordering = ["-created_at"]
    
    # ✅ READ-ONLY PROPERTY: Get stock from Inventory (Single Source of Truth)
    @property
    def in_stock(self):
        """
        Get current stock quantity from Inventory model.
        This is a READ-ONLY property - do NOT assign to it.
        To update stock, use: product.inventory.current_quantity = value
        """
        try:
            if hasattr(self, 'inventory') and self.inventory:
                return self.inventory.current_quantity or 0.0
        except Exception:
            pass
        return 0.0
    
    @property
    def available_stock(self):
        """
        Get available stock for sale (current_quantity - reserved_quantity).
        This considers reserved stock from pending orders.
        """
        try:
            if hasattr(self, 'inventory') and self.inventory:
                return self.inventory.available_quantity
        except Exception:
            pass
        return 0.0
    
    @property
    def is_low_stock(self):
        """Check if product stock is below minimum threshold."""
        try:
            if hasattr(self, 'inventory') and self.inventory:
                return self.inventory.is_low_stock
        except Exception:
            pass
        return False
    
    @property
    def is_out_of_stock(self):
        """Check if product is out of stock."""
        try:
            if hasattr(self, 'inventory') and self.inventory:
                return self.inventory.is_out_of_stock
        except Exception:
            pass
        return True
    
    # ✅ HELPER METHODS for stock management
    def update_stock(self, quantity, reason="", user=None):
        """
        Helper method to set stock to a specific quantity.
        Creates InventoryTransaction for audit trail.
        
        Usage: product.update_stock(quantity=100, reason="Stock count", user=request.user)
        """
        from .inventory import Inventory, InventoryTransaction
        
        inventory, created = Inventory.objects.get_or_create(
            product=self,
            defaults={'current_quantity': quantity, 'min_quantity': 0.0, 'reserved_quantity': 0.0}
        )
        
        old_quantity = inventory.current_quantity
        inventory.current_quantity = quantity
        inventory.save(update_fields=['current_quantity', 'updated_at'])
        
        # Log transaction
        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type='adjust',
            quantity=quantity - old_quantity,
            reason=reason or "Stock adjustment",
            created_by=user
        )
        
        return inventory
    
    def add_stock(self, quantity, reason="", reference_number="", user=None):
        """
        Helper method to add stock (e.g., goods receipt).
        
        Usage: product.add_stock(quantity=50, reason="Goods receipt", user=request.user)
        """
        from .inventory import Inventory, InventoryTransaction
        
        inventory, created = Inventory.objects.get_or_create(
            product=self,
            defaults={'current_quantity': quantity, 'min_quantity': 0.0, 'reserved_quantity': 0.0}
        )
        
        if not created:
            inventory.current_quantity = (inventory.current_quantity or 0.0) + quantity
            inventory.save(update_fields=['current_quantity', 'updated_at'])
        
        # Log transaction
        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type='in',
            quantity=quantity,
            reference_number=reference_number,
            reason=reason or "Stock in",
            created_by=user
        )
        
        return inventory
    
    def reduce_stock(self, quantity, reason="", reference_number="", user=None):
        """
        Helper method to reduce stock (e.g., order fulfillment).
        
        Usage: product.reduce_stock(quantity=10, reason="Order fulfillment", user=request.user)
        """
        from .inventory import Inventory, InventoryTransaction
        
        inventory = self.inventory
        inventory.current_quantity = max(0, (inventory.current_quantity or 0.0) - quantity)
        inventory.save(update_fields=['current_quantity', 'updated_at'])
        
        # Log transaction
        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type='out',
            quantity=-quantity,
            reference_number=reference_number,
            reason=reason or "Stock out",
            created_by=user
        )
        
        return inventory
