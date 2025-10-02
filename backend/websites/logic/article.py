# logic/article.py
from django.db import transaction
from models.article import Article, ArticleCategory, ArticleTag
from rest_framework.exceptions import NotFound


class ArticleService:
    @staticmethod
    def _set_category_and_tags(article, category_id, tag_ids):
        if category_id:
            try:
                category = ArticleCategory.objects.get(id=category_id)
                article.category = category
            except ArticleCategory.DoesNotExist:
                raise NotFound("Category not found")

        if tag_ids:
            tags = []
            for tag_id in tag_ids:
                try:
                    tag = ArticleTag.objects.get(id=tag_id)
                    tags.append(tag)
                except ArticleTag.DoesNotExist:
                    raise NotFound(f"Tag with ID {tag_id} not found")
            article.tags.set(tags)

        article.save()

    @staticmethod
    def create_article(data, category_id, tag_ids):
        with transaction.atomic():
            article = Article.objects.create(**data)
            ArticleService._set_category_and_tags(article, category_id, tag_ids)
        return article

    @staticmethod
    def update_article(article, data, category_id, tag_ids):
        with transaction.atomic():
            for key, value in data.items():
                setattr(article, key, value)
            ArticleService._set_category_and_tags(article, category_id, tag_ids)
        return article
