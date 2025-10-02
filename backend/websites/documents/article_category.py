from django_opensearch_dsl import fields
from django_opensearch_dsl.registries import registry
from base.documents import BaseDocument
from ..models import ArticleCategory


@registry.register_document
class ArticleCategoryDocument(BaseDocument):
    # Nested object for multilanguaage name
    name = fields.ObjectField(properties={
        'origin': fields.TextField(
            analyzer='standard',
            search_analyzer='standard',
            fields={
                'keyword': fields.KeywordField(),
                'suggest': fields.CompletionField()
            }
        ),
        'created_at': fields.DateField(),
        'updated_at': fields.DateField(),
    })

    # Flat field cho performance
    name_text = fields.TextField(
        analyzer='standard',
        fields={
            'keyword': fields.KeywordField(),
            'suggest': fields.CompletionField()
        }
    )

    # Description field
    description = fields.TextField(
        analyzer='standard',
        fields={
            'keyword': fields.KeywordField()
        }
    )

    # Slug field
    slug = fields.KeywordField()

    # Metadata fields
    created_at = fields.DateField()
    updated_at = fields.DateField()

    class Index:
        name = 'websites_article_categories'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'max_result_window': 10000
        }

    class Django:
        model = ArticleCategory
        fields = []

    def prepare_name_text(self, instance):
        """Prepare flat name field"""
        if instance.name:
            return instance.name.origin
        return ""

    def prepare_description(self, instance):
        """Prepare description field"""
        return instance.description or ""

    def prepare_slug(self, instance):
        """Prepare slug field"""
        return instance.slug or ""

    def prepare_created_at(self, instance):
        """Prepare created_at field"""
        return instance.created_at

    def prepare_updated_at(self, instance):
        """Prepare updated_at field"""
        return instance.updated_at

    def prepare(self, instance):
        """Custom prepare method"""
        data = super().prepare(instance)

        # Handle name object structure
        if instance.name:
            data['name'] = {
                'origin': instance.name.origin,
                'created_at': instance.name.created_at,
                'updated_at': instance.name.updated_at,
            }
        else:
            data['name'] = {
                'origin': '',
                'created_at': None,
                'updated_at': None,
            }

        return data
    
    @classmethod
    def get_query_set(cls, **kwargs):
        """
        Use AI Search to get the best match results then convert them to query set.
        Get kwargs as parameters and return a query set.
        """
        keyword = kwargs.get('keyword', None)
        # Build search query
        search = cls.search()

        # Multi-strategy search for better results
        search_query = {
            "bool": {
                "should": [
                    # Strategy 1: Exact phrase match (highest priority)
                    {
                        "multi_match": {
                            "query": keyword,
                            "fields": ["name.origin.keyword^5", "name_text.keyword^5"],
                            "type": "phrase",
                            "boost": 3.0
                        }
                    },
                    # Strategy 2: Best fields match with boost
                    {
                        "multi_match": {
                            "query": keyword,
                            "fields": [
                                "name.origin^4",
                                "name_text^4",
                                "description^2",
                                "slug^3"
                            ],
                            "type": "best_fields",
                            "fuzziness": "AUTO",
                            "boost": 2.0
                        }
                    },
                    # Strategy 3: Cross fields for complex queries
                    {
                        "multi_match": {
                            "query": keyword,
                            "fields": [
                                "name.origin^2",
                                "description",
                                "slug"
                            ],
                            "type": "cross_fields",
                            "operator": "and",
                            "boost": 1.5
                        }
                    },
                    # Strategy 4: Wildcard search for partial matching
                    {
                        "wildcard": {
                            "name.origin": {
                                "value": f"*{keyword.lower()}*",
                                "boost": 1.0
                            }
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        }

        s = search.query(search_query)
        return s.to_queryset()