from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.status import (
    HTTP_200_OK
)

from common.constants.client_constants import  client_constants as common_client_constants
from oauth.constants.client_constants import client_constants as oauth_client_constants
from hr.constants.client_constants import client_constants as hr_client_constants
from knowledge.constants.client_constants import client_constants as knowledge_client_constants
from ecommerce.constants.client_constants import client_constants as ecommerce_client_constants
from websites.constants.client_constants import client_constants as website_client_constants
from va.constants.client_constants import client_constants as va_client_constants

client_constants= {
    **common_client_constants,
    **oauth_client_constants,
    **hr_client_constants,
    **knowledge_client_constants,
    **ecommerce_client_constants,
    **website_client_constants,
    **va_client_constants
}

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def index(request, *args, **kwargs):
    names = request.query_params.get('names', None)
    if names is None:
        return Response( client_constants, status=HTTP_200_OK)
    names = names.split(',')
    
    filtered_constants = {key: value for key, value in client_constants.items() if key in names}
    return Response( filtered_constants, status=HTTP_200_OK)
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def retrieve(request, *args, **kwargs):
    name = kwargs.get('name', None)
    if name is None:
        raise MethodNotAllowed()
    value = client_constants.get(name, None)
    if value is None:
        raise NotFound(_("Constant were not found."))
    return Response(value, status=HTTP_200_OK)

