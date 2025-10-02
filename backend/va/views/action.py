from base.views.base import BaseViewSet
from ..models import Action
from ..serializers import ActionSerializer

class ActionViewSet(BaseViewSet):
    queryset = Action.objects.all() 
    serializer_class= ActionSerializer
    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }