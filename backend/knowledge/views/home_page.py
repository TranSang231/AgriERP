from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from base.views import BaseViewSet
from common.constants import Http
from ..models import HomePage
from ..serializers import HomePageSerializer

User = get_user_model()

class HomePageViewSet(BaseViewSet):
    queryset = HomePage.objects.all()
    search_map = {
        "namespace__name": "icontains",
        "content": "icontains"
    }
    serializer_class = HomePageSerializer
    required_alternate_scopes = {
        "list": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]],
        "retrieve": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]],
        "create": [["knowledge:namespaces:edit"]],
        "update": [["knowledge:namespaces:edit"]],
        "destroy": [["knowledge:namespaces:edit"]],
        "retrieve_by_namespace": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]],
    }

    @action(detail=False, methods=[Http.HTTP_GET], url_path="namespaces/(?P<namespace_pk>[^/.]+)")
    def retrieve_by_namespace(self, request, *args, **kwargs):
        """
        Retrieve hompage by namespace id
        """
        namespace_pk = kwargs.get('namespace_pk')
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {'namespace_id': namespace_pk}
        obj = get_object_or_404(queryset, **filter_kwargs)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)