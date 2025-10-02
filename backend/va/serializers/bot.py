from ..models import Bot
from rest_framework import serializers


class BotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bot
        fields = ['id', 'name', 'config','output_folder', 'created_at', 'updated_at']
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            'name': {'required': False}
        }
