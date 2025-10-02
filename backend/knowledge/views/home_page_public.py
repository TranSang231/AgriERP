from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from common.constants import Http
from base.views import ViewOnlyViewSet
from ..models import HomePage
from ..serializers import HomePageSerializer
from ..filters import PublicAcessFilterBackend

User = get_user_model()

class HomePagePublicViewSet(ViewOnlyViewSet):
    authentication_classes=[]
    permission_classes=[AllowAny]
    queryset = HomePage.objects.all()
    filter_backends = [PublicAcessFilterBackend]
    search_map = {
        "namespace__name": "icontains",
        "content": "icontains"
    }
    serializer_class = HomePageSerializer
    required_alternate_scopes = {
        "list": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]],
        "retrieve": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]]
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
