from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from base.views import ViewOnlyViewSet
from ..models import Namespace
from ..serializers import NamespaceSerializer, NamespaceShortSerializer
from ..filters import PublicAcessFilterBackend

User = get_user_model()

class NamespacePublicViewSet(ViewOnlyViewSet):
    authentication_classes=[]
    permission_classes=[AllowAny]
    queryset = Namespace.objects.all()
    filter_backends = [PublicAcessFilterBackend]
    search_map = {
        "name": "icontains",
        "description": "icontains"
    }
    serializer_class = NamespaceSerializer
    serializer_map = {
        "list": NamespaceShortSerializer,
    }
    required_alternate_scopes = {
        "list": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]],
        "retrieve": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]]
    }
