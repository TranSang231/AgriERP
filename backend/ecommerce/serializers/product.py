from rest_framework import serializers
from django.conf import settings
from base.serializers import WritableNestedSerializer
from contents.serializers import ShortContentSerializer, LongContentSerializer
from ..models import ProductCategory, Product
from .product_category import ProductCategorySerializer
from .product_image import ProductImageSerializer
from .promotion import PromotionSerializer
from .inventory import InventoryShortSerializer


class ProductSerializer(WritableNestedSerializer):
    name = ShortContentSerializer(required=False)
    unit = ShortContentSerializer(required=False)
    images = ProductImageSerializer(many=True, required=False)
    description = LongContentSerializer(required=False)
    categories = ProductCategorySerializer(many=True, required=False)
    category_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=ProductCategory.objects.all(),
                                                   source='categories')
    promotions = PromotionSerializer(many=True, required=False, read_only=True)
    inventory = InventoryShortSerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField()
    
    # ✅ READ-ONLY fields from Product @property (reads from Inventory)
    in_stock = serializers.SerializerMethodField()
    available_stock = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()
    is_out_of_stock = serializers.SerializerMethodField()
    
    def get_in_stock(self, obj):
        """Get stock from Inventory via Product.in_stock property"""
        return obj.in_stock  # Calls @property which reads from Inventory
    
    def get_available_stock(self, obj):
        """Get available stock (current - reserved)"""
        return obj.available_stock
    
    def get_is_low_stock(self, obj):
        """Check if stock is low"""
        return obj.is_low_stock
    
    def get_is_out_of_stock(self, obj):
        """Check if stock is out"""
        return obj.is_out_of_stock
    
    def get_thumbnail(self, obj):
        """Return absolute API URL for thumbnail with normalized path."""
        if obj.thumbnail:
            thumbnail_path = obj.thumbnail.name.replace("\\", "/")
            default_host = getattr(settings, "DEFAULT_HOST", "localhost:8008")
            default_scheme = getattr(settings, "DEFAULT_SCHEME", "http")
            url = f"{default_scheme}://{default_host}/api/v1/files/{thumbnail_path}"
            print(f"[DEBUG ProductSerializer] Generated thumbnail URL: {url}")
            return url
        return None
    
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "thumbnail",
            "images",
            "description",
            "price",
            "unit",
            "in_stock",  # READ-ONLY via SerializerMethodField
            "available_stock",  # NEW: available for sale
            "is_low_stock",  # NEW: low stock indicator
            "is_out_of_stock",  # NEW: out of stock indicator
            "categories",
            "category_ids",
            "promotions",
            "inventory",
            "weight",
            "length",
            "width",
            "height",
            "tax_rate",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'thumbnail': {'required': False},
            'price': {'required': False},
            'weight': {'required': False},
            'length': {'required': False},
            'width': {'required': False},
            'height': {'required': False},
            'tax_rate': {'required': False}
        }
        read_only_fields = ["id", "promotions", "in_stock", "available_stock", "is_low_stock", "is_out_of_stock", "created_at", "updated_at"]
        nested_create_fields = ["name", "unit", "images", "description"]
        nested_update_fields = ["name", "unit", "images", "description"]