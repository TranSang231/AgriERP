
from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Bot, Intent
from .utterance import UtteranceSerializer


class IntentTrainigSerializer(serializers.ModelSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Bot.objects.all(),
                                                   pk_field=UUIDField(format='hex'), source='bot')
    utterances  = UtteranceSerializer(many=True, required=False)
    class Meta:
        model = Intent
        fields = ['id', 'name', 'utterances', 'bot_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': False}
        }
