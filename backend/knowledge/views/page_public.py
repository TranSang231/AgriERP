from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from base.views import ViewOnlyViewSet
from ..models import Page
from ..serializers import PageSerializer, PageShortSerializer
from ..filters import PublicAcessFilterBackend

User = get_user_model()

class PagePublicViewSet(ViewOnlyViewSet):
    authentication_classes=[]
    permission_classes=[AllowAny]
    queryset = Page.objects.all()
    filter_backends = [PublicAcessFilterBackend]
    search_map = {
        "name": "icontains",
        "description": "icontains"
    }
    serializer_class = PageSerializer
    serializer_map = {
        "list": PageShortSerializer,
    }
    required_alternate_scopes = {
        "list": [["knowledge:pages:view"], ["knowledge:pages:edit"]],
        "retrieve": [["knowledge:pages:view"], ["knowledge:pages:edit"]]
    }
