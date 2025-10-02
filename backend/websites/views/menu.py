from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from common.constants import Http

from websites.models.menu import Menu
from websites.serializers.menu import MenuSerializer
from base.views.base import BaseViewSet
from ..filters import SiteFilterBackend


class MenuViewSet(BaseViewSet):
    queryset = Menu.objects.all()
    queryset_map = {
        "list": Menu.objects.all().order_by("order")
    }
    filter_backends = [SiteFilterBackend]
    serializer_class = MenuSerializer
    required_alternate_scopes = {
        "create": [["websites:sites:edit"]],
        "update": [["websites:sites:edit"]],
        "destroy": [["websites:sites:edit"]],

    }
        
    def get_permissions(self):
        """Every one can see the list and detail of memu"""

        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()

