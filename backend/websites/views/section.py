from base.views import BaseViewSet

from ..models import Section
from ..serializers import SectionSerializer
from..filters import SiteFilterBackend



class SectionViewSet(BaseViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = [SiteFilterBackend]

    required_alternate_scopes = {
        "list": [["websites:sites:view"], ["websites:sites:edit"]],
        "retrieve": [["websites:sites:view"], ["websites:sites:edit"]],
        "create": [["websites:sites:edit"]],
        "update": [["websites:sites:edit"]],
        "destroy": [["websites:sites:edit"]]
    }

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
