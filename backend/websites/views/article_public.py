from rest_framework.permissions import AllowAny
from base.views import ViewOnlyViewSet

from ..models import Article
from ..serializers import ArticleSerializer
from ..filters import SiteFilterBackend



class ArticlePublicViewSet(ViewOnlyViewSet):
    authentication_classes=[]
    permission_classes=[AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [SiteFilterBackend]

    required_alternate_scopes = {
        "list": [["websites:articles:view"], ["websites:articles:edit"]],
        "retrieve": [["websites:articles:view"], ["websites:articles:edit"]]
    }
