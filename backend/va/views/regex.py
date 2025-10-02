from django.shortcuts import render
from base.views.base import BaseViewSet
from ..models import Regex
from ..serializers import RegexSerializer
from ..filters import BotFilterBackend

class RegexViewSet(BaseViewSet):
    queryset = Regex.objects.all() 
    serializer_class= RegexSerializer
    filter_backends = [BotFilterBackend]
    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistantss:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }