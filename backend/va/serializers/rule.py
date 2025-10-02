from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from ..models import Bot, Rule
from .rule_step import RuleStepSerializer


class RuleSerializer(WritableNestedSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Bot.objects.all(),
        source='bot'
    )
    steps = RuleStepSerializer(many=True, required=False)

    class Meta:
        model = Rule
        fields = [
            'id',
            'name',
            'steps',
            'conversation_start',
            'wait_for_user_input',
            'bot_id',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'name': {'required': False},
            'conversation_start': {'required': False},
            'wait_for_user_input': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["steps"]
        nested_update_fields = ["steps"]
