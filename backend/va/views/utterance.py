from base.views.base import BaseViewSet
from ..models import Utterance
from ..serializers import UtteranceSerializer
from ..filters import BotFilterBackend

class UtteranceViewSet(BaseViewSet):
    queryset = Utterance.objects.all() 
    serializer_class= UtteranceSerializer
    filter_backends = [BotFilterBackend]
    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }