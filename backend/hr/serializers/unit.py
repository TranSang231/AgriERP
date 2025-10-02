from rest_framework import serializers
from rest_framework.fields import UUIDField, IntegerField
from businesses.serializers.employee import EmployeeShortSerializer
from hr.models.unit_type import UnitType
from hr.models.unit import Unit
from businesses.models.employee import Employee
from base.serializers.writable_nested import WritableNestedSerializer
from .unit_type import UnitTypeSerializer
from base.serializers.recursive import RecursiveSerializer
class UnitSerializer(WritableNestedSerializer):
    type = UnitTypeSerializer(read_only=True, required=False)
    type_id = serializers.PrimaryKeyRelatedField(required=False,
                                                queryset=UnitType.objects.all(),
                                                source='type')
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    manager = EmployeeShortSerializer(required=False)
    manager_id = serializers.PrimaryKeyRelatedField(required=False,
                                                allow_null=True,
                                                queryset=Employee.objects.all(),
                                                source='manager')
    members = EmployeeShortSerializer(many=True, required=False)
    member_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True,
                                                   allow_empty=True, queryset=Employee.objects.all(), source='members')                                
                                                  
    class Meta:
        model = Unit
        fields = [
            "id",
            "type",
            "type_id",
            "parent_id",
            "name",
            "email",
            "slack_channel",
            "manager",
            "manager_id",
            "members",
            "member_ids",
        ]
        extra_kwargs = {
            'name': {'required': False},
            'email': {'required': False},
            'slack_channel': {'required': False, "allow_null": True},
        }
        

class UnitTreeSerializer(serializers.ModelSerializer):
    type = UnitTypeSerializer(read_only=True, required=False)
    type_id = serializers.PrimaryKeyRelatedField(required=False,
                                                queryset=UnitType.objects.all(),
                                                source='type')
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    manager = EmployeeShortSerializer(required=False)
    manager_id = serializers.PrimaryKeyRelatedField(required=False,
                                                queryset=Employee.objects.all(),
                                                source='manager')
    members = EmployeeShortSerializer(many=True, required=False)
    member_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True, allow_empty=True,queryset=Employee.objects.all(), source='members')                                  
    units = RecursiveSerializer(many=True)
    class Meta:
        model = Unit
        fields = [
            "id",
            "type",
            "type_id",
            "parent_id",
            "name",
            "email",
            "slack_channel",
            "manager",
            "manager_id",
            "members",
            "member_ids",
            "units",
        ]
        extra_kwargs = {
            'type': {'required': False},
            'name': {'required': False},
            'email': {'required': False, "allow_null": True},
            'slack_channel': {'required': False, "allow_null": True},
            'units': {'required': False},
        }

