from django.urls import path, include
from rest_framework_nested import routers
from base.routers import NestedMutipleUpdateRouter

from .views import UserTokenViewSet

app_name = 'firebase'
router = routers.SimpleRouter(trailing_slash=False)

router.register(r'user-tokens', UserTokenViewSet, basename="user-tokens")

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
]
