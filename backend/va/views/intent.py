from django.shortcuts import render
from base.views.base import BaseViewSet
from ..models import Intent
from ..serializers import IntentSerializer
from ..filters import BotFilterBackend

class IntentViewSet(BaseViewSet):
    queryset = Intent.objects.all() 
    serializer_class= IntentSerializer
    filter_backends = [BotFilterBackend]
    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }