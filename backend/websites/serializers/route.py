# serializers/article.py
from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from contents.serializers import ShortContentSerializer, LongContentSerializer
from ..models.site import Site
from ..models.route import Route 
from .site import SiteSerializer


class RouteSerializer(WritableNestedSerializer):
    title = ShortContentSerializer(required=False)
    description = ShortContentSerializer(required=False, allow_null=True)
    content = LongContentSerializer(required=False, allow_null=True)
    site_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Site.objects.all(),
        source='site'
    )

    class Meta:
        model = Route
        fields = [
            "id",
            "path",
            "title",
            "description",
            "keywords",
            "content",
            "status",
            "site_id",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'path': {'required': False},
            'keywords': {'required': False},
            'status': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["title", "description", "content"]
        nested_update_fields = ["title", "description", "content"]
