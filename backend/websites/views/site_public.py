from rest_framework.permissions import AllowAny
from base.views import ViewOnlyViewSet
from ..models import Site
from ..serializers import SiteSerializer
from ..filters import DomainFilterBackend


class SitePublicViewSet(ViewOnlyViewSet):
    authentication_classes=[]
    permission_classes=[AllowAny]
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    filter_backends = [DomainFilterBackend]
    
    required_alternate_scopes = {
        "list": [["websites:sites:view"], ["websites:sites:edit"]],
        "retrieve": [["websites:sites:view"], ["websites:sites:edit"]]
    }
