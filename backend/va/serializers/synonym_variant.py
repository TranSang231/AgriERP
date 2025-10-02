from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Synonym, SynonymVariant


class SynonymVariantSerializer(serializers.ModelSerializer):
    synonym_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Synonym.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='synonym'
    )
    
    class Meta:
        model = SynonymVariant
        fields = ['id', 'value', 'synonym_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'value': {'required': False}
        }
