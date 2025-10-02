from ..serializers import EmployeeAdditionalInformationSerializer
from base.views.base import BaseViewSet


class EmployeeAdditionalInformationViewSet(BaseViewSet):
    serializer_class = EmployeeAdditionalInformationSerializer
    required_alternate_scopes = {
        "create": [["employees:edit"], ["employees:edit-mine"]],
        "update": [["employees:edit"], ["employees:edit-mine"]],
        "destroy": [["employees:edit"], ["employees:edit-mine"]],
        "list": [["employees:view"]],
        "retrieve": [["employees:view"], ["employees:view-mine"]],
    }

