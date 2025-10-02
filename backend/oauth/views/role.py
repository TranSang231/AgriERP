from base.views import BaseViewSet
from ..permissions import IsAdministrator
from ..models.role import Role
from ..serializers.role import RoleSerializer
from rest_framework import status
from rest_framework.response import Response


class RoleViewSet(BaseViewSet):
    queryset = Role.objects.exclude(name__exact="Super Administrator")
    search_map = {
        "name": "icontains",
        "description": "icontains"
    }
    serializer_class = RoleSerializer
    required_alternate_scopes = {
        "list": [["roles:view"], ["roles:edit"]],
        "retrieve": [["roles:view"], ["roles:edit"]],
        "create": [["roles:edit"]],
        "update": [["roles:edit"]],
        "destroy": [["roles:edit"]],
    }

    def get_permissions(self):
        """
        All administrators can see the roles
        """
        if self.action in ["list", "retrieve"]:
            return [IsAdministrator()]
        else :
            return super().get_permissions()
