from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.public_product import PublicProductViewSet, PublicProductCategoryViewSet

# Public API router - no authentication required
public_router = DefaultRouter()
public_router.register(r'products', PublicProductViewSet, basename='public-products')
public_router.register(r'categories', PublicProductCategoryViewSet, basename='public-categories')

urlpatterns = [
    path('public/', include(public_router.urls)),
]
