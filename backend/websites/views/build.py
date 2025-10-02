from base.views import BaseViewSet
from ..models import Build
from ..serializers import BuildSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..filters import SiteFilterBackend


class BuildViewSet(BaseViewSet):
    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    filter_backends = [SiteFilterBackend]
    
    required_alternate_scopes = {
        "list": [["websites:sites:view"], ["websites:sites:edit"]],
        "retrieve": [["websites:sites:view"], ["websites:sites:edit"]],
        "create": [["websites:sites:edit"]],
        "update": [["websites:sites:edit"]],
        "destroy": [["websites:sites:edit"]],
        "deploy": [["websites:sites:edit"]]
    }

    ## This api action will trigger deploy process
    ## POST api/v1/websites/builds/[build-id]/deploy
    @action(methods=['post'], detail=True, url_path="deploy", url_name="deploy")
    def deploy(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(self.get_object(), data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                self.get_object().deploy()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                data = {
                    "type": type(e).__name__,
                    "message": str(e)
                }
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)