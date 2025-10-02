from rest_framework.decorators import action
from rest_framework.response import Response
from common.constants import Http
from base.views.base import BaseViewSet
from ..models import Bot
from ..serializers import BotSerializer, BotTrainingSerializer

class BotViewSet(BaseViewSet):
    queryset = Bot.objects.all() 
    serializer_class= BotSerializer
    serializer_map = {
        "training_data": BotTrainingSerializer,
    }
    required_alternate_scopes = {
        "create": [["virtual-assistants:edit"]],
        "retrieve": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "update": [["virtual-assistants:edit"]],
        "destroy": [["virtual-assistants:edit"]],
        "list": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "training_data": [["virtual-assistants:view"], ["virtual-assistants:edit"]]
    }

    @action(detail=True, methods=[Http.HTTP_GET], url_path="training-data")
    def training_data(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    