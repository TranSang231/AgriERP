from rest_framework import serializers
from ..models import ShortContent
from .short_translate import ShortTranslateSerializer
from base.serializers import WritableNestedSerializer

class ShortContentSerializer(WritableNestedSerializer):
    translates = ShortTranslateSerializer(many=True,required = False)

    class Meta:
        model = ShortContent
        fields = ['id', 'origin', 'translates']
        extra_kwargs = {
            'origin': {'required': False}
        }
        nested_create_fields=["translates"]
        nested_update_fields = ["translates"]
