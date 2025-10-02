from ..models import LongContent
from .long_translate import LongTranslateSerializer
from base.serializers import WritableNestedSerializer


class LongContentSerializer(WritableNestedSerializer):
    translates = LongTranslateSerializer(many=True, required=False)

    class Meta:
        model = LongContent
        fields = ["id", "origin", "translates", "attachments"]
        extra_kwargs = {
            'origin': {'required': False},
            'attachments': {'required': False}
        }
        nested_create_fields = ["translates"]
        nested_update_fields = ["translates"]
