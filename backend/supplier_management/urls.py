from django.urls import path, include
from rest_framework_nested import routers
from .views import SupplierViewSet 

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'suppliers', SupplierViewSet, basename="suppliers") 

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
]