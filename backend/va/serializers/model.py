from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Bot, NLUModel


class NLUModelSerializer(serializers.ModelSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Bot.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='bot'
    )
    class Meta:
        model = NLUModel
        fields = ['id', 'name' , 'hash', 'file' , 'bot_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': False},
            'hash': {'required': False},
            'file': {'required': False}
        }
        read_only_fields = ['id', 'file', 'hash', 'created_at', 'updated_at']
