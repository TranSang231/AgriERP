from rest_framework.permissions import AllowAny
from websites.models.menu import Menu
from websites.serializers.menu import MenuSerializer
from base.views import ViewOnlyViewSet
from ..filters import SiteFilterBackend, DomainFilterBackend


class MenuPublicViewSet(ViewOnlyViewSet):
    authentication_classes=[]
    permission_classes=[AllowAny]
    queryset = Menu.objects.all()
    queryset_map = {
        "list": Menu.objects.all().order_by("order")
    }
    filter_backends = [SiteFilterBackend, DomainFilterBackend]
    serializer_class = MenuSerializer
    required_alternate_scopes = {
        "create": [["websites:sites:edit"]],
        "update": [["websites:sites:edit"]],
        "destroy": [["websites:sites:edit"]],

    }
