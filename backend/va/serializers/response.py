from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Bot, Response


class ResponseSerializer(serializers.ModelSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Bot.objects.all(),
                                                   pk_field=UUIDField(format='hex'), source='bot')
    class Meta:
        model = Response
        fields = ['id', 'name', 'text', 'image', 'custom', 'bot_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': False},
            'text': {'required': False},
            'image': {'required': False},
            'custom': {'required': False}
        }
