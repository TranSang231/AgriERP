from django.urls import path, include
from rest_framework_nested import routers

from .views import (
    NamespaceViewSet,
    NamespacePublicViewSet,
    PageViewSet,
    PagePublicViewSet,
    HomePageViewSet,
    HomePagePublicViewSet,
    StatisticViewSet
)


app_name = "knowledge"
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"namespaces", NamespaceViewSet, basename="knowledge-namespaces")
router.register(r"pages", PageViewSet, basename="knowledge-pages")
router.register(r"home-pages", HomePageViewSet, basename="knowledge-hone-pages")
router.register(r"statistics", StatisticViewSet, basename="knowledge-statistics")

public_router = routers.SimpleRouter(trailing_slash=False)
public_router.register(r"namespaces", NamespacePublicViewSet, basename="knowledge-public-namespaces")
public_router.register(r"pages", PagePublicViewSet, basename="knowledge-public-pages")
public_router.register(r"home-pages", HomePagePublicViewSet, basename="knowledge-public-hone-pages")

urlpatterns = [
    path(r'api/v1/knowledge/', include(router.urls)),
    path(r'api/public/v1/knowledge/', include(public_router.urls))
]
