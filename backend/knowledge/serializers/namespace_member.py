# serializers/article.py
from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from rest_framework.fields import UUIDField
from businesses.models import Employee
from ..models.namespace_member import NamespaceMember
from businesses.serializers import EmployeeShortSerializer

class NamespaceMemberSerializer(WritableNestedSerializer):
    namespace_id = serializers.UUIDField(required=False, allow_null=True)
    employee = EmployeeShortSerializer(required=False)
    employee_id = serializers.PrimaryKeyRelatedField(
        required=False,
        write_only=True,
        allow_null=True,
        allow_empty=True,
        queryset=Employee.objects.all(),
        source='employee'
    )

    class Meta:
        model = NamespaceMember
        fields = [
            "id",
            "namespace_id",
            "employee",
            "employee_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]