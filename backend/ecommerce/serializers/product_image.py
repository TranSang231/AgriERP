from rest_framework import serializers
from rest_framework.fields import UUIDField
from django.conf import settings
from ..models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Product.objects.all(),
        source='product'
    )
    image = serializers.SerializerMethodField()
    
    def get_image(self, obj):
        """Return absolute API URL for image with normalized path."""
        if obj.image:
            image_path = obj.image.name.replace("\\", "/")
            default_host = getattr(settings, "DEFAULT_HOST", "localhost:8008")
            default_scheme = getattr(settings, "DEFAULT_SCHEME", "http")
            url = f"{default_scheme}://{default_host}/api/v1/files/{image_path}"
            print(f"[DEBUG ProductImageSerializer] Generated image URL: {url}")  # DEBUG
            return url
        return None
    
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