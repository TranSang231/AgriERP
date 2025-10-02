from base.views.base import BaseViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from ..models import UserToken
from ..serializers import UserTokenSerializer
from ..filters import UserTokenFilterBackend
from ..services import CloudMessageService


class UserTokenViewSet(BaseViewSet):
    queryset = UserToken.objects.all()
    serializer_class = UserTokenSerializer
    filter_backends = [UserTokenFilterBackend]

    required_alternate_scopes = {
        "create": [["employees:edit"]],
        "update": [["employees:edit"]],
        "destroy": [["employees:edit"]],
        "retrieve": [["employees:view"], ["employees:edit"]],
        "list": [["employees:view"], ["employees:edit"]],
        "test_message": [["employees:edit"]],
    }

    @action(detail=False, methods=["post"], url_path='test-message')
    def test_message(self, request, *args, **kwargs):
        # Extract title and body from request query parameters
        title = request.data.get('title', 'Default Title')
        body = request.data.get('body', 'Default Body')

        # Send the cloud message with the custom title and body
        message = CloudMessageService.send_cloud_message(
            user_id=request.auth.user.id, title=title, body=body, local_image_path="media/notification/Logo.jpg")

        # Return a response indicating success or failure
        return Response({"message": message}, status=status.HTTP_200_OK)
