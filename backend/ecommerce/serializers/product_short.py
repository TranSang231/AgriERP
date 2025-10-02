from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from ..models import ProductCategory, Product
from contents.serializers import ShortContentSerializer, LongContentSerializer
from .product_category import ProductCategorySerializer

class ProductShortSerializer(WritableNestedSerializer):
    name = ShortContentSerializer(required=False)
    unit = ShortContentSerializer(required=False)
    categories = ProductCategorySerializer(many=True, required=False)
    category_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=ProductCategory.objects.all(),
                                                   source='categories')
    
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "thumbnail",
            "price",
            "unit",
            "in_stock",
            "categories",
            "category_ids",
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
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["name", "unit", "images", "description"]
        nested_update_fields = ["name", "unit", "images", "description"]