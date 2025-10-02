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
        read_only_fields = ["id", "promotions", "created_at", "updated_at"]
        nested_create_fields = ["name", "unit", "images", "description"]
        nested_update_fields = ["name", "unit", "images", "description"]