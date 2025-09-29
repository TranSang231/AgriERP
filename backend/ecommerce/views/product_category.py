from base.views import BaseViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from ..models import ProductCategory
from ..serializers import ProductCategorySerializer

class ProductCategoryViewSet(BaseViewSet):
    queryset = ProductCategory.objects.all()
    search_map = {
        "name__origin": "icontains"
    }
    serializer_class = ProductCategorySerializer
    required_alternate_scopes = {
        "list": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "retrieve": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "create": [["ecommerce:products:edit"]],
        "update": [["ecommerce:products:edit"]],
        "destroy": [["ecommerce:products:edit"]],
        "with_product_count": [["ecommerce:products:view"], ["ecommerce:products:edit"]]
    }

    def get_permissions(self):
        """Allow public access for listing and viewing product categories."""
        if self.action in ["list", "retrieve", "with_product_count"]:
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['GET'], url_path="with-product-count")
    def with_product_count(self, request, *args, **kwargs):
        """Get categories with their product counts"""
        include_empty = request.query_params.get('include_empty', 'true').lower() == 'true'
        
        queryset = self.get_queryset().annotate(
            product_count=Count('products', distinct=True),
            active_product_count=Count(
                'products', 
                filter=Q(products__is_active=True),
                distinct=True
            )
        )
        
        if not include_empty:
            queryset = queryset.filter(product_count__gt=0)
        
        queryset = queryset.order_by('-product_count', 'name__origin')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Add product counts to serialized data
            data = serializer.data
            for i, item in enumerate(data):
                item['product_count'] = page[i].product_count
                item['active_product_count'] = page[i].active_product_count
            return self.get_paginated_response(data)
        
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for i, item in enumerate(data):
            item['product_count'] = queryset[i].product_count
            item['active_product_count'] = queryset[i].active_product_count
        
        return Response(data, status=status.HTTP_200_OK)