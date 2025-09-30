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
        ).distinct()[:12]  
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="on-sale")
    def on_sale(self, request, *args, **kwargs):
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

    @action(detail=False, methods=['GET'], url_path="new-arrivals")
    def new_arrivals(self, request, *args, **kwargs):
        from datetime import timedelta
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        queryset = self.get_queryset().filter(
            created_at__gte=thirty_days_ago
        ).order_by('-created_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="by-category/(?P<category_id>[^/.]+)")
    def by_category(self, request, category_id=None, *args, **kwargs):
        if not category_id:
            return Response(
                {"error": "category_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            category_id = int(category_id)
            queryset = self.get_queryset().filter(categories__id=category_id)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid category_id format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['GET'], url_path="search")
    def search(self, request, *args, **kwargs):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response(
                {"error": "Search query 'q' parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(
            Q(name__origin__icontains=query) |
            Q(description__origin__icontains=query) |
            Q(categories__name__origin__icontains=query)
        ).distinct()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="filter")
    def filter_products(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        params = request.query_params
        
        min_price = params.get('min_price')
        max_price = params.get('max_price')
        
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except (ValueError, TypeError):
                pass
        
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except (ValueError, TypeError):
                pass
        
        in_stock = params.get('in_stock')
        if in_stock and in_stock.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(in_stock__gt=0)
        
        category_ids = params.get('category_ids')
        if category_ids:
            try:
                category_ids = [int(id.strip()) for id in category_ids.split(',') if id.strip()]
                queryset = queryset.filter(categories__id__in=category_ids).distinct()
            except (ValueError, TypeError):
                pass
        
        has_promotion = params.get('has_promotion')
        if has_promotion and has_promotion.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(
                promotion_items__promotion__start__lte=timezone.now(),
                promotion_items__promotion__end__gte=timezone.now()
            ).distinct()
        
        sort_by = params.get('sort_by', 'name')
        sort_order = params.get('sort_order', 'asc')
        
        if sort_by in ['name', 'price', 'created_at', 'in_stock']:
            if sort_order == 'desc':
                sort_by = f'-{sort_by}'
            queryset = queryset.order_by(sort_by)
        
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
        queryset = self.get_queryset().annotate(
            active_product_count=Count(
                'products', 
                distinct=True
            )
        ).filter(active_product_count__gt=0).order_by('name__origin')
        
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        # Add product count to response
        for i, item in enumerate(data):
            item['active_product_count'] = queryset[i].active_product_count
        
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="stats")
    def stats(self, request, *args, **kwargs):
        from django.db.models import Count, Q, Avg
        
        total_categories = ProductCategory.objects.count()
        total_products = Product.objects.count()
        products_on_sale = Product.objects.filter(
            promotion_items__promotion__start__lte=timezone.now(),
            promotion_items__promotion__end__gte=timezone.now()
        ).distinct().count()
        products_in_stock = Product.objects.filter(in_stock__gt=0).count()
        
        price_stats = Product.objects.aggregate(
            min_price=Min('price'),
            max_price=Max('price'),
            avg_price=Avg('price')
        )
        
        stats = {
            'total_categories': total_categories,
            'total_products': total_products,
            'products_on_sale': products_on_sale,
            'products_in_stock': products_in_stock,
            'price_range': {
                'min': price_stats.get('min_price', 0),
                'max': price_stats.get('max_price', 0),
                'average': round(price_stats.get('avg_price', 0), 2) if price_stats.get('avg_price') else 0
            }
        }
        
        return Response(stats, status=status.HTTP_200_OK)
