from base.serializers import WritableNestedSerializer
from ..models import Province
from .province_mapping import ProvinceMappingSerializer

class ProvinceSerializer(WritableNestedSerializer):
    mapping = ProvinceMappingSerializer(many=True, required=False, source='provincemapping_set')

    class Meta:
        model = Province
        fields = [
            "id",
            "name",
            "mapping",
            "created_at",
            "updated_at"
        ]
        
        extra_kwargs = {
            'name': {'required': False}
        }

        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["mapping"]
        nested_update_fields = ["mapping"]
