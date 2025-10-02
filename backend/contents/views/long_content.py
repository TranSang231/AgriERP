from base.views.base import BaseViewSet
from contents.models import LongContent
from rest_framework.permissions import AllowAny
from contents.serializers import LongContentSerializer

# Create your views here.
class LongContentViewSet(BaseViewSet):
    queryset = LongContent.objects.all() 
    serializer_class= LongContentSerializer
    required_alternate_scopes = {
        "create": [["admin:contents:edit"]],
        "retrieve": [["admin:contents:view"], ["admin:contents:edit"]],
        "update": [["admin:contents:edit"]],
        "destroy": [["admin:contents:edit"]],
        "list": [["admin:contents:view"], ["admin:contents:edit"]],
    }