from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Bot, Conversation

class ConversationSerializer(serializers.ModelSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Bot.objects.all(),
                                                   pk_field=UUIDField(format='hex'), source='bot')
    class Meta:
        model = Conversation
        fields = ['id', 'story' , 'conversation', 'bot_id']
