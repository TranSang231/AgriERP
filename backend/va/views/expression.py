from django.shortcuts import render
from base.views.base import BaseViewSet
from ..models import Expression
from ..serializers import ExpressionSerializer

class ExpressionViewSet(BaseViewSet):
    queryset = Expression.objects.all() 
    serializer_class= ExpressionSerializer
    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
    }