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
        "on_sale": [["ecommerce:products:view"], ["ecommerce:products:edit"]]
    }

    def get_permissions(self):
        """Allow public access for listing and viewing products."""
        if self.action in ["list", "retrieve", "summary_list"]:
            return [AllowAny()]
        return super().get_permissions()

    def processParams(self, request):
        """Override to add custom price range filtering."""
        queryset, page_size = super().processParams(request)
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