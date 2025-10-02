from rest_framework.permissions import AllowAny
from base.views import ViewOnlyViewSet
from ..models import Section
from ..serializers import SectionSerializer
from..filters import SiteFilterBackend, DomainFilterBackend



class SectionPublicViewSet(ViewOnlyViewSet):
    authentication_classes=[]
    permission_classes=[AllowAny]
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = [SiteFilterBackend, DomainFilterBackend]

    required_alternate_scopes = {
        "list": [["websites:sites:view"], ["websites:sites:edit"]],
        "retrieve": [["websites:sites:view"], ["websites:sites:edit"]]
    }

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
