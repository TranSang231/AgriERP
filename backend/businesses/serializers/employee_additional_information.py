from rest_framework import serializers
from base.serializers import BaseListSerializer, BaseSerializer, MutipleUpdateListSerializer
from ..models import Employee, EmployeeCustomField, EmployeeAdditionalInformation


class EmployeeAdditionalInformationSerializer(BaseSerializer):
    employee_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Employee.objects.all(),
                                                   source='employee')
    field_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=EmployeeCustomField.objects.all(),
                                                   source='field')

    class Meta:
        model = EmployeeAdditionalInformation
        list_serializer_class = MutipleUpdateListSerializer
        fields = ['id', 'employee', 'employee_id', 'field', 'field_id', 'value']
        extra_kwargs = {
            'employee': {'required': False},
            'field': {'required': False},
        }
        depth = 1

