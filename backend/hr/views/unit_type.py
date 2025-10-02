from hr.models.unit_type import UnitType
from base.views import BaseViewSet
from hr.serializers.unit_type import UnitTypeSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
#

class UnitTypeViewSet(BaseViewSet):
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    search_map = {
        "name": "icontains",
        "description": "icontains",
    }

    required_alternate_scopes = {
        "create": [["organization:edit"]],
        "retrieve": [["organization:view"], ["organization:edit"]],
        "update": [["organization:edit"]],
        "destroy": [["organization:edit"]],
        "list": [["organization:view"], ["organization:edit"]],
        "multiple_delele": [["organization:edit"]],
    }
        
