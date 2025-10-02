
from base.views import BaseViewSet
from ..models import Application
from ..serializers import ApplicationSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from drf_nested_forms.utils import NestedForm
from oauth2_provider.generators import generate_client_secret


class ApplicationViewSet(BaseViewSet):

    queryset = Application.objects.all()
    search_map = {
        "name": "icontains",
        "description": "icontains"
    }
    serializer_class = ApplicationSerializer
    required_alternate_scopes = {
        "list": [["admin:applications:view"], ["admin:applications:edit"]],
        "retrieve": [["admin:applications:view"], ["admin:applications:edit"]],
        "create": [["admin:applications:edit"]],
        "update": [["admin:applications:edit"]],
        "destroy": [["admin:applications:edit"]],
    }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        content_type = request.content_type
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data
        # This secret key will be hashed before store to database
        # Make sure to inform user to store it somewhere, because they can't get it again
        client_secret = generate_client_secret()
        data.update({"client_secret": client_secret})
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            self.clear_querysets_cache()
            return Response(
                {
                    "client_secret": client_secret,
                    "application": serializer.data
                },
                status=HTTP_201_CREATED
            )
