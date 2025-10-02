from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework.permissions import AllowAny
from common.constants import Http
from base.views.base import BaseViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_500_INTERNAL_SERVER_ERROR
from ..models import EmailOTPDevice
from ..serializers import EmailOTPDeviceSerializer


class EmailOTPDeviceViewSet(BaseViewSet):
    queryset = EmailOTPDevice.objects.all()
    serializer_class = EmailOTPDeviceSerializer
    required_alternate_scopes = {
        "create": [["admin:otp:devices:edit"]],
        "update": [["admin:otp:devices:edit"]],
        "destroy": [["admin:otp:devices:edit"]],
        "retrieve": [["admin:otp:devices:edit"]],
        "list": [["admin:otp:devices:edit"]]
    }

    @action(
        detail=False,
        methods=[Http.HTTP_POST],
        url_path="send",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def send(self, request, *args, **kwargs):
        email = request.data.get("email")
        try:
            device, created = EmailOTPDevice.objects.get_or_create(email=email)
            device.generate_challenge()
        except Exception as e:
            print(e)
            return Response(
                {"message": _("There is an error occur.")},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response({"message": _("The OTP have been sent.")}, status=HTTP_200_OK)

    @action(
        detail=False,
        methods=[Http.HTTP_POST],
        url_path="verify",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def verify(self, request, *args, **kwargs):
        email = request.data.get("email")
        token = request.data.get("token")
        try:
            device, created = EmailOTPDevice.objects.get_or_create(email=email)
            verify = device.verify_token(token)
            if verify:
                return Response(
                    {"message": _("Your email is verified successfully.")},
                    status=HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": _("Your OTP is not valid or expired.")},
                    status=HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            print(e)
            return Response(
                {"message": _("There is an error occur.")},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
