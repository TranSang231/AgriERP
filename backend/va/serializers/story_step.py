from rest_framework import serializers
from ..models import Story, StoryStep


class StoryStepSerializer(serializers.ModelSerializer):
    story_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Story.objects.all(),
        source='story'
    )
    class Meta:
        model = StoryStep
        fields = ['id', 'order', 'type', 'payload' , 'story_id']
        extra_kwargs = {
            'order': {'required': False},
            'type': {'required': False},
            'payload': {'required': False}
        }
