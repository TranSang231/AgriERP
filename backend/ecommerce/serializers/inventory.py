from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from ..models import Inventory, InventoryTransaction, Product


class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = [
            'id', 'transaction_type', 'quantity', 'reference_number', 
            'reason', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InventorySerializer(WritableNestedSerializer):
    product = serializers.SerializerMethodField()
    transactions = InventoryTransactionSerializer(many=True, read_only=True)
    available_quantity = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    is_out_of_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'product', 'current_quantity', 'min_quantity', 'max_quantity',
            'reserved_quantity', 'available_quantity', 'is_low_stock', 'is_out_of_stock',
            'transactions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_product(self, obj):
        """Get product details - handles deleted products and categories gracefully"""
        try:
            # Check if product exists
            if not obj.product:
                return {
                    'id': None,
                    'name': 'Product Deleted',
                    'price': 0,
                    'unit': None,
                    'thumbnail': None,
                    'categories': []
                }
            
            product = obj.product
            
            # Safely get product name with nested try-except
            product_name = None
            try:
                if hasattr(product, 'name') and product.name:
                    product_name = str(product.name)
            except (AttributeError, Exception):
                pass
            
            # Fallback to product ID if name retrieval failed
            if not product_name:
                try:
                    product_name = f"Product #{product.id}"
                except Exception:
                    product_name = "Unknown Product"
            
            # Safely get categories with comprehensive error handling
            categories = []
            try:
                if hasattr(product, 'categories'):
                    # Use select_related/prefetch_related already done at viewset level
                    for cat in product.categories.all():
                        try:
                            # Validate category exists
                            if not cat:
                                continue
                                
                            cat_name = None
                            try:
                                # Try to get category name
                                if hasattr(cat, 'name') and cat.name:
                                    cat_name = str(cat.name)
                            except (AttributeError, Exception):
                                pass
                            
                            # Fallback name
                            if not cat_name:
                                try:
                                    cat_name = f"Category #{cat.id}"
                                except Exception:
                                    cat_name = "Unknown Category"
                            
                            # Add category to list
                            categories.append({
                                'id': cat.id if cat else None,
                                'name': cat_name
                            })
                        except Exception:
                            # Skip this category entirely if any error
                            continue
            except (AttributeError, Exception):
                # Product might not have categories relationship
                categories = []
            
            # Safely get thumbnail
            thumbnail = None
            try:
                if hasattr(product, 'thumbnail') and product.thumbnail:
                    thumbnail = product.thumbnail.url
            except (AttributeError, Exception):
                thumbnail = None
            
            # Safely get price
            price = 0
            try:
                if hasattr(product, 'price'):
                    price = product.price
            except (AttributeError, Exception):
                price = 0
            
            # Safely get unit
            unit = None
            try:
                if hasattr(product, 'unit') and product.unit:
                    unit = str(product.unit)
            except (AttributeError, Exception):
                unit = None
            
            return {
                'id': product.id if product else None,
                'name': product_name,
                'price': price,
                'unit': unit,
                'thumbnail': thumbnail,
                'categories': categories
            }
            
        except Exception as e:
            # If anything goes wrong, return a minimal safe structure
            try:
                return {
                    'id': obj.product.id if hasattr(obj, 'product') and obj.product else None,
                    'name': 'Error loading product',
                    'price': 0,
                    'unit': None,
                    'thumbnail': None,
                    'categories': []
                }
            except Exception:
                return None


class InventoryShortSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    product_sku = serializers.SerializerMethodField()
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'product', 'product_name', 'product_price', 'product_sku',
            'current_quantity', 'min_quantity', 'max_quantity', 'available_quantity',
            'is_low_stock', 'is_out_of_stock', 'updated_at'
        ]

    def get_product_name(self, obj):
        """Get product name - handles deleted products gracefully"""
        try:
            # Check if product exists
            if not obj.product:
                return "Product Deleted"
            
            # Try to get product name
            try:
                if hasattr(obj.product, 'name') and obj.product.name:
                    return str(obj.product.name)
            except (AttributeError, Exception):
                pass
            
            # Fallback to product ID
            try:
                return f"Product #{obj.product.id}"
            except Exception:
                return "Unknown Product"
                
        except Exception:
            return "Unknown"

    def get_product_price(self, obj):
        """Get product price - handles deleted products gracefully"""
        try:
            if not obj.product:
                return 0
            
            if hasattr(obj.product, 'price'):
                try:
                    return obj.product.price
                except (AttributeError, Exception):
                    return 0
        except Exception:
            pass
        return 0

    def get_product_sku(self, obj):
        """Get product SKU - handles deleted products gracefully"""
        try:
            if not obj.product:
                return "N/A"
            
            # You might want to add SKU field to Product model
            if obj.product:
                try:
                    return f"SKU-{obj.product.id}"
                except Exception:
                    return "N/A"
        except Exception:
            pass
        return "N/A"
