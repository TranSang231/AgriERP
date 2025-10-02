from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework.permissions import AllowAny
from common.constants import Http
from base.views.base import BaseViewSet
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from ..models import PhoneOTPDevice
from ..serializers import PhoneOTPDeviceSerializer


class PhoneOTPDeviceViewSet(BaseViewSet):
    queryset = PhoneOTPDevice.objects.all()
    serializer_class = PhoneOTPDeviceSerializer
    required_alternate_scopes = {
        "create": [["admin:otp:devices:edit"]],
        "update": [["admin:otp:devices:edit"]],
        "destroy": [["admin:otp:devices:edit"]],
        "retrieve": [["admin:otp:devices:edit"]],
        "list": [["admin:otp:devices:edit"]]
    }

    @action(detail=False, methods=[Http.HTTP_POST], url_path="send-sms", permission_classes=[AllowAny], authentication_classes=[])
    def send_sms(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        country_code = request.data.get("country_code", "84")
        if phone.startswith('0'):
            phone = "+" + country_code  + phone[1:]
        
        try:
            device, created = PhoneOTPDevice.objects.get_or_create(phone=phone)
            device.generate_challenge()
        except Exception as e:
            print(e)
            return Response({"message": _("There is an error occur.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": _("The OTP have been sent.")}, status=HTTP_200_OK)