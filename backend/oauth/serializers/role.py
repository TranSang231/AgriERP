from ..models.role import Role
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "description",
            "scope",
            "last_modified_by",
            "updated_at",
        ]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
            "scope": {"required": False},
            "last_modified_by": {"required": False},
            "updated_at": {"read_only": True},
        }


class RoleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "description",
            "updated_at",
        ]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
            "updated_at": {"read_only": True},
        }