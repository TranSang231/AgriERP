from base.views.base import BaseViewSet
from ..models import Rule
from ..serializers import RuleSerializer
from ..filters import BotFilterBackend

class RuleViewSet(BaseViewSet):
    queryset = Rule.objects.all() 
    serializer_class= RuleSerializer
    filter_backends = [BotFilterBackend]

    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }