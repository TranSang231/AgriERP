from base.serializers import WritableNestedSerializer
from ..models import ProductCategory
from contents.serializers import ShortContentSerializer

class ProductCategorySerializer(WritableNestedSerializer):
    name = ShortContentSerializer(required=False)

    class Meta:
        model = ProductCategory
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'description': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["name"]
        nested_update_fields = ["name"]