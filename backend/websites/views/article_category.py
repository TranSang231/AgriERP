from base.views import AISearchViewSet, BaseViewSet

from ..models import ArticleCategory
from ..serializers import ArticleCategorySerializer
from ..documents import ArticleCategoryDocument


class ArticleCategoryViewSet(AISearchViewSet, BaseViewSet):
    queryset = ArticleCategory.objects.all()
    document_class = ArticleCategoryDocument
    search_map = {
        "name__origin": "icontains",
        "description": "icontains"
    }
    serializer_class = ArticleCategorySerializer
    required_alternate_scopes = {
        "list": [["websites:sites:view"], ["websites:sites:edit"]],
        "retrieve": [["websites:sites:view"], ["websites:sites:edit"]],
        "create": [["websites:sites:edit"]],
        "update": [["websites:sites:edit"]],
        "destroy": [["websites:sites:edit"]]
    }
