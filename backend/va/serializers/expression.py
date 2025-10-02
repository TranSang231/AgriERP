from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Intent, Expression


class ExpressionSerializer(serializers.ModelSerializer):
    intent_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Intent.objects.all(),
                                                   pk_field=UUIDField(format='hex'), source='intent')
    class Meta:
        model = Expression
        fields = ['id', 'text' , 'intent_id']
        extra_kwargs = {
            'text': {'required': False}
        }
