from ..models import EmployeeCustomField
from ..serializers import EmployeeCustomFieldSerializer
from base.views.base import MultipleUpdateViewSet


class EmployeeCustomFieldViewSet(MultipleUpdateViewSet):
    queryset = EmployeeCustomField.objects.all()
    serializer_class = EmployeeCustomFieldSerializer
    required_alternate_scopes = {
        "create": [["employees:edit"]],
        "update": [["employees:edit"]],
        "destroy": [["employees:edit"]],
        "list": [["employees:view"], ["employees:edit"]],
        "retrieve": [["employees:view"], ["employees:edit"]],
        "sync": [["employees:edit"]],
        "multiple_delele": [["employees:edit"]],
    }

