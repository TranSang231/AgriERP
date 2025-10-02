from base.views import BaseViewSet

from ..models import Article
from ..serializers import ArticleSerializer
from ..filters import SiteFilterBackend



class ArticleViewSet(BaseViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [SiteFilterBackend]

    required_alternate_scopes = {
        "list": [["websites:articles:view"], ["websites:articles:edit"]],
        "retrieve": [["websites:articles:view"], ["websites:articles:edit"]],
        "create": [["websites:articles:edit"]],
        "update": [["websites:articles:edit"]],
        "destroy": [["websites:articles:edit"]]
    }
