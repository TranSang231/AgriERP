from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q, Avg, Min, Max
from django.utils import timezone

from ..models import Product, ProductCategory
from ..serializers import ProductSerializer, ProductShortSerializer, ProductCategorySerializer


class PublicProductViewSet(ReadOnlyModelViewSet):
    """
    Public API for products - no authentication required.
    Provides read-only access to products for shop frontend.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        """Use short serializer for list views to improve performance"""
        if self.action == 'list':
            return ProductShortSerializer
        return ProductSerializer

    def get_queryset(self):
        """Get all products with related data"""
        return Product.objects.all().select_related().prefetch_related(
            'categories',
            'promotion_items__promotion',
            'images'
        )

    @action(detail=False, methods=['GET'], url_path="featured")
    def featured(self, request, *args, **kwargs):
        """Get featured products (products with promotions or high ratings)"""
        queryset = self.get_queryset().filter(
            Q(promotion_items__promotion__start__lte=timezone.now()) &
            Q(promotion_items__promotion__end__gte=timezone.now())
        ).distinct()[:12]  # Limit to 12 featured products
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="on-sale")
    def on_sale(self, request, *args, **kwargs):
        """Get products currently on sale with active promotions"""
        queryset = self.get_queryset().filter(
            promotion_items__promotion__start__lte=timezone.now(),
            promotion_items__promotion__end__gte=timezone.now()
        ).distinct()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="search")
    def search(self, request, *args, **kwargs):
        """Search products by name, description, or category"""
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response(
                {"error": "Search query 'q' parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(categories__name__translations__icontains=query)
        ).distinct()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicProductCategoryViewSet(ReadOnlyModelViewSet):
    """
    Public API for product categories - no authentication required.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['GET'], url_path="with-products")
    def with_products(self, request, *args, **kwargs):
        """Get categories that have active products"""
        queryset = self.get_queryset().annotate(
            active_product_count=Count('products', distinct=True)
        ).filter(active_product_count__gt=0).order_by('name__origin')
        
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        # Add product count to response
        for i, item in enumerate(data):
            item['active_product_count'] = queryset[i].active_product_count
        
        return Response(data, status=status.HTTP_200_OK)
