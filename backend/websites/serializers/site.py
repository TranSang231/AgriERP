from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from contents.serializers import ShortContentSerializer
from .section import SectionShortSerializer
from ..models.site import Site


class SiteSerializer(WritableNestedSerializer):
    title = ShortContentSerializer(required=False)
    description = ShortContentSerializer(required=False)
    sections = SectionShortSerializer(many=True, required=False)

    class Meta:
        model = Site
        fields = [
            "id",
            "domain_name",
            "title",
            "description",
            "keywords",
            "icon",
            "template",
            "template_settings",
            "sections",
            "status",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'domain_name': {'required': False},
            'keywords': {'required': False},
            'icon': {'required': False},
            'template': {'required': False},
            'template_settings': {'required': False},
            'status': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["title", "description", "sections"]
        nested_update_fields = ["title", "description", "sections"]


class SiteShortSerializer(WritableNestedSerializer):
    title = ShortContentSerializer(required=False)
    description = ShortContentSerializer(required=False)

    class Meta:
        model = Site
        fields = [
            "id",
            "domain_name",
            "title",
            "description",
            "keywords",
            "icon",
            "status",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'domain_name': {'required': False},
            'keywords': {'required': False},
            'icon': {'required': False},
            'status': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["title", "description"]
        nested_update_fields = ["title", "description"]
