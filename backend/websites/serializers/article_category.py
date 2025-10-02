# serializers/article.py
from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from contents.serializers import ShortContentSerializer
from ..models.article import ArticleCategory


class ArticleCategorySerializer(WritableNestedSerializer):
    name = ShortContentSerializer(required=False)

    class Meta:
        model = ArticleCategory
        fields = ["id", "name", "slug", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["name"]
        nested_update_fields = ["name"]