# serializers/article.py
from rest_framework import serializers
from rest_framework.fields import UUIDField
from base.serializers import WritableNestedSerializer
from contents.serializers import ShortContentSerializer, LongContentSerializer
from ..models.site import Site
from ..models.article_category import ArticleCategory 
from ..models.article import Article 
from .article_category import ArticleCategorySerializer
from .site import SiteSerializer


class ArticleSerializer(WritableNestedSerializer):
    title = ShortContentSerializer(required=False)
    categories = ArticleCategorySerializer(many=True, required=False)
    category_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=ArticleCategory.objects.all(), pk_field=UUIDField(format='hex'),
                                                   source='categories')
    description = ShortContentSerializer(required=False, allow_null=True)
    content = LongContentSerializer(required=False, allow_null=True)
    sites = SiteSerializer(many=True, required=False)
    site_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=Site.objects.all(), pk_field=UUIDField(format='hex'),
                                                   source='sites')

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
            "sites",
            "site_ids",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'slug': {'required': False},
            'keywords': {'required': False},
            'thumbnail': {'required': False},
            'status': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["title", "description", "content"]
        nested_update_fields = ["title", "description", "content"]
