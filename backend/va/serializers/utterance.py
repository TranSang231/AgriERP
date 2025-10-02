from rest_framework import serializers
from ..models import Bot, Intent, Utterance
from .utterance_entity import UtteranceEntitySerializer
from base.serializers import WritableNestedSerializer

class UtteranceSerializer(WritableNestedSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Bot.objects.all(),
        source='bot'
    )
    intent_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Intent.objects.all(),
        source='intent'
    )
    entities = UtteranceEntitySerializer(
        many=True,
        required=False,
        source="utterance_entities"
    )
    class Meta:
        model = Utterance
        fields = ['id', 'text' , 'entities', 'bot_id', 'intent_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'text': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["entities"]
        nested_update_fields = ["entities"]
