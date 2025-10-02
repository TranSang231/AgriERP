from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from ..models import Site, Build


class BuildSerializer(WritableNestedSerializer):
    site_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Site.objects.all(),
        source='site')
    site_id = serializers.UUIDField(required=False)

    class Meta:
        model = Build
        fields = [
            "id",
            "archive",
            "info",
            "status",
            "site_id",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'archive': {'required': False},
            'info': {'required': False},
            'status': {'required': False},
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_update_fields = []