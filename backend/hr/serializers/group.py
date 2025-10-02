from rest_framework import serializers
from rest_framework.fields import UUIDField

from ..models import Group, Office
from base.serializers.recursive import RecursiveSerializer
from businesses.serializers import EmployeeSerializer
from .office import OfficeShortSerializer

from businesses.models.employee import Employee

class GroupSerializer(serializers.ModelSerializer):
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    manager = EmployeeSerializer(read_only=True, required=False)
    manager_id = serializers.PrimaryKeyRelatedField(required=False,
                                                queryset=Employee.objects.all(),
                                                source='manager')
    offices = OfficeShortSerializer(many=True, required=False)
    office_ids = serializers.PrimaryKeyRelatedField(required=False, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=Office.objects.all(),
                                                   source='offices')
    
    class Meta:
        model = Group
        fields = [
            "id",
            "parent_id",
            "name",
            "email",
            "manager",
            "manager_id",
            "offices",
            "office_ids",
        ]
        extra_kwargs = {
            'name': {'required': False},
            'email': {'required': False, "allow_null": True},
            'groups': {'required': False},
        }


class GroupTreeSerializer(serializers.ModelSerializer):
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    manager = EmployeeSerializer(read_only=True, required=False)
    manager_id = serializers.PrimaryKeyRelatedField(required=False,
                                                queryset=Employee.objects.all(),
                                                source='manager')
    offices = OfficeShortSerializer(many=True, required=False)
    office_ids = serializers.PrimaryKeyRelatedField(required=False, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=Office.objects.all(),
                                                   source='offices')
    groups = RecursiveSerializer(many=True)
    class Meta:
        model = Group
        fields = [
            "id",
            "parent_id",
            "name",
            "email",
            "manager",
            "manager_id",
            "offices",
            "office_ids",
            "groups",
        ]
        extra_kwargs = {
            'name': {'required': False},
            'email': {'required': False, "allow_null": True},
            'groups': {'required': False},
        }