from base.serializers import WritableNestedSerializer
from ..models import Ward
from .ward_mapping import WardMappingSerializer

class WardSerializer(WritableNestedSerializer):
    mapping = WardMappingSerializer(many=True, required=False, source='warkmapping_set')

    class Meta:
        model = Ward
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
