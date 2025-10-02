from rest_framework import serializers
from ..models import Utterance, Entity, UtteranceEntity
from .entity import EntitySerializer

class UtteranceEntitySerializer(serializers.ModelSerializer):
    utterance_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Utterance.objects.all(),
        source='utterance'
    )
    entity = EntitySerializer(required=False)
    entity_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Entity.objects.all(),
        source='entity'
    )
    class Meta:
        model = UtteranceEntity
        fields = ['id', 'text', 'start' , 'end', 'style', 'utterance_id', 'entity',  'entity_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'entity', 'created_at', 'updated_at']
        extra_kwargs = {
            'text': {'required': False},
            'start': {'required': False},
            'end': {'required': False},
            'style': {'required': False}
        }
