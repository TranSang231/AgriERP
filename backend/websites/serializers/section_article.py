from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from rest_framework.fields import UUIDField
from ..models.article import Article
from..models.section_article import SectionArticle
from .article_short import ArticleShortSerializer

class SectionArticleSerializer(WritableNestedSerializer):
    section_id = serializers.UUIDField(required=False, allow_null=True)
    article = ArticleShortSerializer(required=False)
    article_id = serializers.PrimaryKeyRelatedField(
        required=False,
        write_only=True,
        allow_null=True,
        allow_empty=True,
        queryset=Article.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='article'
    )

    class Meta:
        model = SectionArticle
        fields = [
            "id",
            "section_id",
            "article",
            "article_id",
            "order",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'order': {'required': False},
        }
        read_only_fields = ["id", "created_at", "updated_at"]