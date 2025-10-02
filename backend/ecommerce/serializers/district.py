from base.serializers import WritableNestedSerializer
from ..models import District
from .district_mapping import DistrictMappingSerializer

class DistrictSerializer(WritableNestedSerializer):
    mapping = DistrictMappingSerializer(many=True, required=False, source='districtmapping_set')

    class Meta:
        model = District
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
