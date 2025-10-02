from base.views import BaseViewSet
from ..models import Page
from ..serializers import PageSerializer, PageShortSerializer

class PageViewSet(BaseViewSet):
    queryset = Page.objects.all()
    search_map = {
        "title": "icontains",
        "description": "icontains"
    }
    serializer_class = PageSerializer
    serializer_map = {
        "list": PageShortSerializer,
    }
    required_alternate_scopes = {
        "list": [["knowledge:pages:view"], ["knowledge:pages:edit"]],
        "retrieve": [["knowledge:pages:view"], ["knowledge:pages:edit"]],
        "create": [["knowledge:pages:edit"]],
        "update": [["knowledge:pages:edit"]],
        "destroy": [["knowledge:pages:edit"]]
    }