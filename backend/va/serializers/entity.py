from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Bot, Entity

class EntitySerializer(serializers.ModelSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Bot.objects.all(),
                                                   pk_field=UUIDField(format='hex'), source='bot')
    class Meta:
        model = Entity
        fields = ['id', 'name' , 'slot_data_type', 'bot_id']
        extra_kwargs = {
            'name': {'required': False},
            'slot_data_type': {'required': False}
        }
