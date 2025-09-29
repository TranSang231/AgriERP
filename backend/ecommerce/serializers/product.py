from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from contents.serializers import ShortContentSerializer, LongContentSerializer
from ..models import ProductCategory, Product
from .product_category import ProductCategorySerializer
from .product_image import ProductImageSerializer
from .promotion import PromotionSerializer


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
    sale_price = serializers.SerializerMethodField()
    has_promotion = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "thumbnail",
            "images",
            "description",
            "price",
            "sale_price",
            "has_promotion",
            "discount_percentage",
            "unit",
            "in_stock",
            "categories",
            "category_ids",
            "promotions",
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
        read_only_fields = ["id", "promotions", "sale_price", "has_promotion", "discount_percentage", "created_at", "updated_at"]
        nested_create_fields = ["name", "unit", "images", "description"]
        nested_update_fields = ["name", "unit", "images", "description"]

    def get_sale_price(self, obj):
        """Calculate sale price based on active promotions."""
        from django.utils import timezone
        
        # Get active promotions for this product
        active_promotions = obj.promotion_items.filter(
            promotion__start__lte=timezone.now(),
            promotion__end__gte=timezone.now()
        ).order_by('-discount').first()
        
        if active_promotions and active_promotions.discount > 0:
            discount_factor = (100 - active_promotions.discount) / 100
            return round(obj.price * discount_factor, 2)
        
        return obj.price

    def get_has_promotion(self, obj):
        """Check if product has active promotions."""
        from django.utils import timezone
        
        return obj.promotion_items.filter(
            promotion__start__lte=timezone.now(),
            promotion__end__gte=timezone.now()
        ).exists()

    def get_discount_percentage(self, obj):
        """Get the highest discount percentage from active promotions."""
        from django.utils import timezone
        
        active_promotion = obj.promotion_items.filter(
            promotion__start__lte=timezone.now(),
            promotion__end__gte=timezone.now()
        ).order_by('-discount').first()
        
        return active_promotion.discount if active_promotion else 0