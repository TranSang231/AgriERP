from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from common.constants import Http
from ..services.nlp import NLUService

class NLUPublicViewSet(GenericViewSet):
    authentication_classes=[]
    permission_classes=[AllowAny]

    @action(detail=False, methods=[Http.HTTP_GET], url_path="nlu-host")
    def nul_host(self, request, *args, **kwargs):
        """
        API to get NLU host
        """
        result = NLUService.get_nlu_host()
        return Response(
            {"host": result},
            status=HTTP_200_OK
        )