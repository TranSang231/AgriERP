from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from common.constants import Http
from base.views import BaseViewSet
from ..models import Product
from ..serializers import ProductSerializer, ProductShortSerializer


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    search_map = {
        "name__origin": "icontains",
        "description__origin": "icontains"
    }
    serializer_class = ProductSerializer
    serializer_map = {
        "summary_list": ProductShortSerializer,
    }
    required_alternate_scopes = {
        "list": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "retrieve": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "create": [["ecommerce:products:edit"]],
        "update": [["ecommerce:products:edit"]],
        "destroy": [["ecommerce:products:edit"]],
        "summary_list": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "on_sale": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "by_category": [["ecommerce:products:view"], ["ecommerce:products:edit"]]
    }

    def get_permissions(self):
        """Allow public access for listing and viewing products."""
        if self.action in ["list", "retrieve", "summary_list"]:
            return [AllowAny()]
        return super().get_permissions()

    def processParams(self, request, queryset=None):
        """Override to add custom price range filtering."""
        if queryset is None:
            queryset, page_size = super().processParams(request)
        else:
            page_size = request.query_params.get('page_size')
        params = request.query_params
        
        # Price range filtering
        min_price = params.get('min_price')
        max_price = params.get('max_price')
        
        if min_price is not None:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except (ValueError, TypeError):
                pass  # Ignore invalid price values
                
        if max_price is not None:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except (ValueError, TypeError):
                pass  # Ignore invalid price values
        
        # Stock availability filtering
        in_stock = params.get('in_stock')
        out_of_stock = params.get('out_of_stock')
        
        if in_stock is not None and in_stock.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(in_stock__gt=0)
        elif out_of_stock is not None and out_of_stock.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(in_stock__lte=0)
            
        # Stock quantity filtering
        min_stock = params.get('min_stock')
        if min_stock is not None:
            try:
                min_stock = float(min_stock)
                queryset = queryset.filter(in_stock__gte=min_stock)
            except (ValueError, TypeError):
                pass
        
        # Promotion-based filtering
        has_promotion = params.get('has_promotion')
        promotion_id = params.get('promotion_id')
        min_discount = params.get('min_discount')
        
        if has_promotion is not None and has_promotion.lower() in ['true', '1', 'yes']:
            from django.utils import timezone
            queryset = queryset.filter(
                promotion_items__promotion__start__lte=timezone.now(),
                promotion_items__promotion__end__gte=timezone.now()
            ).distinct()
        
        if promotion_id is not None:
            try:
                promotion_id = int(promotion_id)
                queryset = queryset.filter(promotions__id=promotion_id)
            except (ValueError, TypeError):
                pass
        
        if min_discount is not None:
            try:
                min_discount = float(min_discount)
                from django.utils import timezone
                queryset = queryset.filter(
                    promotion_items__promotion__start__lte=timezone.now(),
                    promotion_items__promotion__end__gte=timezone.now(),
                    promotion_items__discount__gte=min_discount
                ).distinct()
            except (ValueError, TypeError):
                pass
        
        # Category-based filtering
        category_id = params.get('category_id')
        category_ids = params.get('category_ids')
        category_name = params.get('category_name')
        exclude_categories = params.get('exclude_categories')
        
        if category_id is not None:
            try:
                category_id = int(category_id)
                queryset = queryset.filter(categories__id=category_id)
            except (ValueError, TypeError):
                pass
        
        if category_ids is not None:
            try:
                # Support comma-separated list of category IDs
                if isinstance(category_ids, str):
                    category_ids = [int(id.strip()) for id in category_ids.split(',') if id.strip()]
                elif isinstance(category_ids, list):
                    category_ids = [int(id) for id in category_ids]
                queryset = queryset.filter(categories__id__in=category_ids).distinct()
            except (ValueError, TypeError):
                pass
        
        if category_name is not None:
            # Search by category name (using ShortContent relationship)
            queryset = queryset.filter(
                categories__name__translations__icontains=category_name
            ).distinct()
        
        if exclude_categories is not None:
            try:
                # Support comma-separated list of category IDs to exclude
                if isinstance(exclude_categories, str):
                    exclude_ids = [int(id.strip()) for id in exclude_categories.split(',') if id.strip()]
                elif isinstance(exclude_categories, list):
                    exclude_ids = [int(id) for id in exclude_categories]
                queryset = queryset.exclude(categories__id__in=exclude_ids)
            except (ValueError, TypeError):
                pass
        
        return queryset, page_size

    @action(detail=False, methods=[Http.HTTP_GET], url_path="summary-list")
    def summary_list(self, request, *args, **kwargs):
        queryset, page_size = self.processParams(request);
        if page_size is not None:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=[Http.HTTP_GET], url_path="on-sale")
    def on_sale(self, request, *args, **kwargs):
        """Get products that are currently on sale (have active promotions)."""
        from django.utils import timezone
        
        queryset = self.get_queryset().filter(
            promotion_items__promotion__start__lte=timezone.now(),
            promotion_items__promotion__end__gte=timezone.now()
        ).distinct()
        
        # Apply other filters
        queryset, page_size = self.processParams(request)
        
        if page_size is not None:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=[Http.HTTP_GET], url_path="by-category")
    def by_category(self, request, *args, **kwargs):
        """Get products filtered by category"""
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response(
                {"error": "category_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            category_id = int(category_id)
            queryset = self.get_queryset().filter(categories__id=category_id)
            
            # Apply other filters from processParams
            queryset, page_size = self.processParams(request, queryset=queryset)
            
            if page_size is not None:
                page = self.paginate_queryset(queryset)
                data = self.get_serializer(page, many=True).data
                return self.get_paginated_response(data)
            else:
                data = self.get_serializer(queryset, many=True).data
                return Response(data, status=status.HTTP_200_OK)
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid category_id format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )