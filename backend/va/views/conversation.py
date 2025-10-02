from base.views.base import BaseViewSet
from ..models import Conversation
from ..serializers import ConversationSerializer

class ConversationViewSet(BaseViewSet):
    queryset = Conversation.objects.all() 
    serializer_class= ConversationSerializer
    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }