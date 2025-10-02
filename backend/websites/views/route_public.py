from rest_framework.permissions import AllowAny
from base.views import ViewOnlyViewSet
from ..models import Route
from ..serializers import RouteSerializer
from ..filters import SiteFilterBackend, DomainFilterBackend



class RoutePublicViewSet(ViewOnlyViewSet):
    authentication_classes=[]
    permission_classes=[AllowAny]
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [SiteFilterBackend, DomainFilterBackend]

    required_alternate_scopes = {
        "list": [["websites:sites:view"], ["websites:sites:edit"]],
        "retrieve": [["websites:sites:view"], ["websites:sites:edit"]]
    }
