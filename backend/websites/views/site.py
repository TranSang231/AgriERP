from base.views import BaseViewSet
from ..models import Site
from ..serializers import SiteSerializer


class SiteViewSet(BaseViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    
    required_alternate_scopes = {
        "list": [["websites:sites:view"], ["websites:sites:edit"]],
        "retrieve": [["websites:sites:view"], ["websites:sites:edit"]],
        "create": [["websites:sites:edit"]],
        "update": [["websites:sites:edit"]],
        "destroy": [["websites:sites:edit"]]
    }
