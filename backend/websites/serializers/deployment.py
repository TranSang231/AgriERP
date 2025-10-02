# serializers/article.py
from rest_framework import serializers
from ..models.section import Section


class DeploymentSerializer(serializers.ModelSerializer):
    site_id = serializers.UUIDField(required=False, allow_null=True)

    class Meta:
        model = Section
        fields = [
            "id",
            "data",
            "site_id",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'data': {'required': False},
            'site_id': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
