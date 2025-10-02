from rest_framework import serializers
from base.serializers import MutipleUpdateListSerializer
from ..models import EmployeeCustomField


class EmployeeCustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCustomField
        list_serializer_class = MutipleUpdateListSerializer
        fields = ['id', 'name', 'data_type', 'max_length', 'updated_at']
        extra_kwargs = {
            'name': {'required': False},
            'data_type': {'required': False},
            'max_length': {'required': False},
            'updated_at': {'read_only': True},
        }
        depth = 1

