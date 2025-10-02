from rest_framework import serializers
from oauth.serializers import UserShortSerializer
from ..models import Page,Namespace
from .namespace_short import NamespaceShortSerializer

class PageSerializer(serializers.ModelSerializer):
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    namespace = NamespaceShortSerializer(required=False)
    namespace_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Namespace.objects.all(),
        source='namespace'
    )
    created_by = UserShortSerializer(required=False)
    updated_by = UserShortSerializer(required=False)

    class Meta:
        model = Page
        fields = [
            "id",
            "parent_id",
            "title",
            "slug",
            "content",
            "namespace",
            "namespace_id",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at"
        ]
    
        extra_kwargs = {
            'title': {'required': False},
            'slug': {'required': False},
            'content': {'required': False}
        }

        read_only_fields = ["id", "created_by", "created_at", "updated_by", "updated_at"]