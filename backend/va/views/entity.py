from base.views.base import BaseViewSet
from ..models import Entity
from ..serializers import EntitySerializer
from ..filters import BotFilterBackend

class EntityViewSet(BaseViewSet):
    queryset = Entity.objects.all() 
    serializer_class= EntitySerializer
    filter_backends = [BotFilterBackend]

    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }