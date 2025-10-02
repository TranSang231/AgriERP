from rest_framework import serializers
from ..models import Rule, RuleStep


class RuleStepSerializer(serializers.ModelSerializer):
    rule_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Rule.objects.all(),
        source='rule'
    )
    class Meta:
        model = RuleStep
        fields = ['id', 'order', 'type', 'payload' , 'rule_id']
        extra_kwargs = {
            'order': {'required': False},
            'type': {'required': False},
            'payload': {'required': False}
        }
