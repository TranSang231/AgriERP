from django.urls import include, re_path
from rest_framework_nested import routers

from .views import EmailOTPDeviceViewSet, PhoneOTPDeviceViewSet

app_name = "otp"
router = routers.SimpleRouter(trailing_slash=False)

router.register(r'emails', EmailOTPDeviceViewSet, basename="otp_emails")
router.register(r'phones', PhoneOTPDeviceViewSet, basename="otp_phones")

urlpatterns = [
    re_path(r'^api/v1/otp/', include(router.urls)),
]
