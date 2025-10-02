# serializers/article.py
from rest_framework import serializers
from rest_framework.fields import UUIDField
from base.serializers import WritableNestedSerializer
from contents.serializers import ShortContentSerializer, LongContentSerializer
from ..models.article_category import ArticleCategory 
from ..models.article import Article 
from .article_category import ArticleCategorySerializer

class ArticleShortSerializer(WritableNestedSerializer):
    title = ShortContentSerializer(required=False)
    categories = ArticleCategorySerializer(many=True, required=False)
    category_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=ArticleCategory.objects.all(), pk_field=UUIDField(format='hex'),
                                                   source='categories')
    description = ShortContentSerializer(required=False, allow_null=True)
    content = LongContentSerializer(required=False, allow_null=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "categories",
            "category_ids",
            "description",
            "keywords",
            "thumbnail",
            "content",
            "status",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'slug': {'required': False},
            'keywords': {'required': False},
            'thumbnail': {'required': False, 'allow_null':True},
            'status': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
