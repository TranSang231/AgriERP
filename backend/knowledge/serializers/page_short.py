from rest_framework import serializers
from oauth.serializers import UserShortSerializer
from ..models import Page
from .namespace_short import NamespaceShortSerializer

class PageShortSerializer(serializers.ModelSerializer):
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    namespace = NamespaceShortSerializer(required=False)
    created_by = UserShortSerializer(required=False)
    updated_by = UserShortSerializer(required=False)

    class Meta:
        model = Page
        fields = [
            "id",
            "parent_id",
            "title",
            "slug",
            "namespace",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at"
        ]
    
        extra_kwargs = {
            'title': {'required': False},
            'slug': {'required': False}
        }

        read_only_fields = ["id", "created_by", "created_at", "updated_by", "updated_at"]