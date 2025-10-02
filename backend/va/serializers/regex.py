from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Bot, Regex


class RegexSerializer(serializers.ModelSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Bot.objects.all(),
                                                   pk_field=UUIDField(format='hex'), source='bot')
    class Meta:
        model = Regex
        fields = ['id', 'name','pattern' , 'bot_id', 'created_at', 'updated_at']
        read_only_fields = ["id", "created_at", "updated_at"]