from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from .section_article import SectionArticleSerializer
from ..models import Section


class SectionSerializer(WritableNestedSerializer):
    site_id = serializers.UUIDField(required=False, allow_null=True)
    articles = SectionArticleSerializer(many=True, required=False, source='sectionarticle_set')

    class Meta:
        model = Section
        fields = [
            "id",
            "name",
            "description",
            "articles",
            "site_id",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'site_id': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_update_fields = ["articles"]


class SectionShortSerializer(serializers.ModelSerializer):
    site_id = serializers.UUIDField(required=False, allow_null=True)

    class Meta:
        model = Section
        fields = [
            "id",
            "name",
            "description",
            "site_id",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'site_id': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]