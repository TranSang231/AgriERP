from base.views.base import BaseViewSet
from contents.models import ShortContent
from rest_framework.permissions import AllowAny
from contents.serializers import ShortContentSerializer
    
class ShortContentViewSet(BaseViewSet):
    queryset = ShortContent.objects.all() 
    serializer_class= ShortContentSerializer
    required_alternate_scopes = {
        "create": [["admin:contents:edit"]],
        "retrieve": [["admin:contents:view"], ["admin:contents:edit"]],
        "update": [["admin:contents:edit"]],
        "destroy": [["admin:contents:edit"]],
        "list": [["admin:contents:view"], ["admin:contents:edit"]],
    }