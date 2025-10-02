from base.views import BaseViewSet

from ..models import Route
from ..serializers import RouteSerializer
from ..filters import SiteFilterBackend



class RouteViewSet(BaseViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [SiteFilterBackend]

    required_alternate_scopes = {
        "list": [["websites:sites:view"], ["websites:sites:edit"]],
        "retrieve": [["websites:sites:view"], ["websites:sites:edit"]],
        "create": [["websites:sites:edit"]],
        "update": [["websites:sites:edit"]],
        "destroy": [["websites:sites:edit"]]
    }
