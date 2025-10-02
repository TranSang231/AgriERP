from django.urls import path, re_path, include
from base import routers

# Todo override these default routes to avoid security risk
from oauth2_provider.urls import (
    base_urlpatterns,
    management_urlpatterns,
    oidc_urlpatterns
)

from .views import (
    RoleViewSet,
    UserViewSet,
    ApplicationViewSet
)

app_name = "oauth"
router = routers.MutipleUpdateRouter(trailing_slash=False)

router.register(r"roles", RoleViewSet, basename="roles")
router.register(r"users", UserViewSet, basename="users")
router.register(r"applications", ApplicationViewSet, basename="applications")

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    re_path(r'^api/v1/', include(router.urls)),
]