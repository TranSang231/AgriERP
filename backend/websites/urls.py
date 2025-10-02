# urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    SiteViewSet,
    SitePublicViewSet,
    RouteViewSet,
    RoutePublicViewSet,
    MenuViewSet,
    MenuPublicViewSet,
    ArticleCategoryViewSet,
    ArticleViewSet,
    ArticlePublicViewSet,
    SectionViewSet,
    SectionPublicViewSet,
    BuildViewSet
)

app_name = "websites"
# Private
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"sites", SiteViewSet, basename="sites")
router.register(r"categories", ArticleCategoryViewSet, basename="websites-categories")
router.register(r"routes", RouteViewSet, basename="websites-routes")
router.register(r"menus", MenuViewSet, basename="websites-menus")
router.register(r"articles", ArticleViewSet, basename="websites-articles")
router.register(r"sections", SectionViewSet, basename="websites-sections")
router.register(r"builds", BuildViewSet, basename="websites-builds")

site_router = routers.NestedSimpleRouter(router, r"sites", lookup="sites")
site_router.register(r"routes", RouteViewSet, basename="websites-site-routes")
site_router.register(r"menus", MenuViewSet, basename="websites-site-menus")
site_router.register(r"sections", SectionViewSet, basename="websites-site-sections")
site_router.register(r"articles", ArticleViewSet, basename="websites-site-articles")
site_router.register(r"builds", BuildViewSet, basename="websites-site-builds")

# Public
public_router = routers.SimpleRouter(trailing_slash=False)
public_router.register(r"sites", SitePublicViewSet, basename="websites-public-sites")
public_router.register(r"routes", RoutePublicViewSet, basename="websites-public-routes")
public_router.register(r"menus", MenuPublicViewSet, basename="websites-public-menus")
public_router.register(r"articles", ArticlePublicViewSet, basename="websites-public-articles")
public_router.register(r"sections", SectionPublicViewSet, basename="websites-public-sections")

site_public_router = routers.NestedSimpleRouter(router, r"sites", lookup="sites")
site_public_router.register(r"routes", RoutePublicViewSet, basename="websites-site-public-routes")
site_public_router.register(r"menus", MenuPublicViewSet, basename="websites-site-public-menus")
site_public_router.register(r"articles", ArticlePublicViewSet, basename="websites-site-public-articles")
site_public_router.register(r"sections", SectionPublicViewSet, basename="websites-site-public-sections")

urlpatterns = [
    path(r'api/v1/websites/', include(router.urls)),
    path(r'api/v1/websites/', include(site_router.urls)),
    path(r'api/public/v1/websites/', include(public_router.urls)),
    path(r'api/public/v1/websites/', include(site_public_router.urls))
]
