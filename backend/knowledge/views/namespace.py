from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_nested_forms.utils import NestedForm
from base.views import BaseViewSet
from ..models import Namespace
from ..serializers import NamespaceSerializer, NamespaceShortSerializer

User = get_user_model()

class NamespaceViewSet(BaseViewSet):
    queryset = Namespace.objects.all()
    search_map = {
        "name": "icontains",
        "description": "icontains"
    }
    serializer_class = NamespaceSerializer
    serializer_map = {
        "list": NamespaceShortSerializer,
    }
    required_alternate_scopes = {
        "list": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]],
        "retrieve": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]],
        "create": [["knowledge:namespaces:edit"]],
        "update": [["knowledge:namespaces:edit"]],
        "destroy": [["knowledge:namespaces:edit"]]
    }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        content_type = request.content_type
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data
        # If the space created without owner, we set current user as it owner
        owner_id = data.get("owner_id", None)
        if owner_id is None:
            data.update({"owner_id": request.user.id})
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            self.clear_querysets_cache()
            return Response(serializer.data, status=status.HTTP_201_CREATED)