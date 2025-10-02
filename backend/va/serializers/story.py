from rest_framework import serializers
from rest_framework.fields import UUIDField
from base.serializers import WritableNestedSerializer
from ..models import Bot, Story
from .story_step import StoryStepSerializer


class StorySerializer(WritableNestedSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Bot.objects.all(),
        source='bot'
    )
    steps = StoryStepSerializer(many=True, required=False)

    class Meta:
        model = Story
        fields = ['id', 'name', 'steps', 'bot_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["steps"]
        nested_update_fields = ["steps"]
