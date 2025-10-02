from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Product.objects.all(),
        source='product'
    )
    
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product_id",
            "image",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'image': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]