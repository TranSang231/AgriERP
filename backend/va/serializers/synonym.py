from rest_framework import serializers
from rest_framework.fields import UUIDField
from base.serializers import WritableNestedSerializer
from ..models import Bot, Synonym
from .synonym_variant import SynonymVariantSerializer


class SynonymSerializer(WritableNestedSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Bot.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='bot'
    )
    variants = SynonymVariantSerializer(many=True, required=False)
    
    
    class Meta:
        model = Synonym
        fields = ['id', 'reference', 'variants', 'bot_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'reference': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["variants"]
        nested_update_fields = ["variants"]
