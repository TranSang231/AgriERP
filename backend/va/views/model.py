from django.shortcuts import render
from base.views.base import BaseViewSet
from ..models import NLUModel
from ..serializers import NLUModelSerializer

class NLUModelViewSet(BaseViewSet):
    queryset = NLUModel.objects.all() 
    serializer_class= NLUModelSerializer
    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }