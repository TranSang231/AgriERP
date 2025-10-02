from django.shortcuts import render
from base.views.base import BaseViewSet
from ..models import Story
from ..serializers import StorySerializer
from ..filters import BotFilterBackend

class StoryViewSet(BaseViewSet):
    queryset = Story.objects.all() 
    serializer_class= StorySerializer
    filter_backends = [BotFilterBackend]

    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }