from base.views.base import BaseViewSet
from ..models import Response
from ..serializers import ResponseSerializer
from ..filters import BotFilterBackend

class ResponseViewSet(BaseViewSet):
    queryset = Response.objects.all() 
    serializer_class= ResponseSerializer
    filter_backends = [BotFilterBackend]

    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }