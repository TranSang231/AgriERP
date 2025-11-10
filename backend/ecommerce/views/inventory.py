from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q, Sum, Count
from django.db import transaction
from django.db import models
from common.constants import Http
from base.views import BaseViewSet
from ..models import Inventory, InventoryTransaction, Product, InventoryConfiguration
from ..serializers import (
    InventorySerializer, 
    InventoryShortSerializer, 
    InventoryTransactionSerializer,
    InventoryConfigurationSerializer
)


class InventoryViewSet(BaseViewSet):
    queryset = Inventory.objects.select_related('product').prefetch_related('product__categories')
    search_map = {
        "product__name__origin": "icontains",
    }
    serializer_class = InventorySerializer
    serializer_map = {
        "summary_list": InventoryShortSerializer,
    }
    required_alternate_scopes = {
        "list": [["ecommerce:inventory:view"], ["ecommerce:inventory:edit"]],
        "retrieve": [["ecommerce:inventory:view"], ["ecommerce:inventory:edit"]],
        "create": [["ecommerce:inventory:edit"]],
        "update": [["ecommerce:inventory:edit"]],
        "destroy": [["ecommerce:inventory:edit"]],
        "summary_list": [["ecommerce:inventory:view"], ["ecommerce:inventory:edit"]],
        "adjust_stock": [["ecommerce:inventory:edit"]],
        "get_stats": [["ecommerce:inventory:view"], ["ecommerce:inventory:edit"]],
        "get_low_stock": [["ecommerce:inventory:view"], ["ecommerce:inventory:edit"]],
        "inventory_config": [["ecommerce:inventory:view"], ["ecommerce:inventory:edit"]],
    }

    def get_permissions(self):
        """Allow public access for development"""
        if self.action in ['list', 'retrieve', 'summary_list', 'get_stats', 'get_low_stock', 'inventory_config', 'update', 'partial_update']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def processParams(self, request):
        """Override processParams to handle inventory-specific filters (category_id/category, etc.)"""
        # Get active configuration
        config = InventoryConfiguration.get_active_config()
        
        # Extract category param(s) before parent processes (support both category_id and category)
        raw_category = request.query_params.get('category_id', None)
        if raw_category in (None, "", "null"):
            raw_category = request.query_params.get('category', None)

        # Extract stock status filter
        raw_stock_status = request.query_params.get('stock_status', None)

        # Call parent to handle basic filtering and params
        try:
            queryset, page_size = super().processParams(request)
        except Exception:
            # If parent fails, fall back to default queryset gracefully
            queryset = self.filter_queryset(self.get_queryset())
            page_size = request.query_params.get('page_size', None)

        # Apply category filter only when provided and valid
        invalid_values = {"NaN", "nan", "undefined", "null", "None", "", "Null"}
        if isinstance(raw_category, str):
            candidate = raw_category.strip()
        else:
            candidate = raw_category

        if candidate is not None and (str(candidate) if candidate is not None else "").strip() not in invalid_values:
            # Do NOT cast to int; IDs can be UUID strings. Let Django handle type coercion.
            try:
                queryset = queryset.filter(product__categories__id=candidate).distinct()
            except Exception:
                # If anything goes wrong, ignore the category filter to avoid 500s
                pass

        # Apply stock status filter if provided - using configuration thresholds
        if isinstance(raw_stock_status, str):
            stock_status = raw_stock_status.strip().lower()
            if stock_status and stock_status not in {"nan", "undefined", "null", "none"}:
                try:
                    if stock_status in ("out_of_stock", "out"):
                        queryset = queryset.filter(current_quantity__lte=config.out_of_stock_threshold)
                    elif stock_status in ("low_stock", "low"):
                        # Filter items that are above out_of_stock but at or below their threshold
                        # This is complex because threshold can vary by item, so we do it in Python
                        # For now, use min_quantity as default (most common case)
                        queryset = queryset.filter(
                            current_quantity__gt=config.out_of_stock_threshold,
                            current_quantity__lte=models.F('min_quantity')
                        )
                    elif stock_status in ("in_stock", "in"):
                        queryset = queryset.filter(current_quantity__gt=models.F('min_quantity'))
                    # else: ignore unknown value
                except Exception:
                    # Fail-soft: ignore invalid filter
                    pass

        return queryset, page_size
    
    def list(self, request, *args, **kwargs):
        """Override list to add error handling"""
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': 'Failed to retrieve inventory list: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=[Http.HTTP_GET], url_path="summary-list")
    def summary_list(self
    , request, *args, **kwargs):
        """Get summary list of inventory items"""
        try:
            # Use custom processParams that handles category_id
            queryset, page_size = self.processParams(request)
            if page_size is not None:
                page = self.paginate_queryset(queryset)
                data = self.get_serializer(page, many=True).data
                return self.get_paginated_response(data)
            else:
                data = self.get_serializer(queryset, many=True).data
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Failed to retrieve inventory list: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=[Http.HTTP_GET], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        """Get inventory statistics"""
        try:
            # Get active configuration
            config = InventoryConfiguration.get_active_config()
            
            total_products = self.get_queryset().count()
            low_stock_count = self.get_queryset().filter(
                current_quantity__lte=models.F('min_quantity'),
                current_quantity__gt=config.out_of_stock_threshold
            ).count()
            out_of_stock_count = self.get_queryset().filter(
                current_quantity__lte=config.out_of_stock_threshold
            ).count()
            
            # Calculate total stock value
            total_value = 0
            for inventory in self.get_queryset():
                try:
                    if inventory.product and hasattr(inventory.product, 'price') and inventory.product.price:
                        total_value += inventory.product.price * inventory.current_quantity
                except (AttributeError, Exception):
                    # Product deleted or missing price, skip it
                    continue

            data = {
                'total_products': total_products,
                'total_value': total_value,
                'low_stock_count': low_stock_count,
                'out_of_stock_count': out_of_stock_count,
                'config': {
                    'out_of_stock_threshold': config.out_of_stock_threshold,
                    'low_stock_threshold_type': config.low_stock_threshold_type,
                    'in_stock_label': config.in_stock_label,
                    'low_stock_label': config.low_stock_label,
                    'out_of_stock_label': config.out_of_stock_label,
                }
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=[Http.HTTP_GET], url_path="low-stock")
    def get_low_stock(self, request, *args, **kwargs):
        """Get low stock items"""
        try:
            threshold = float(request.query_params.get('threshold', 10))
            
            low_stock_items = self.get_queryset().filter(
                current_quantity__lte=threshold,
                current_quantity__gt=0
            ).order_by('current_quantity')
            
            serializer = self.get_serializer(low_stock_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=[Http.HTTP_POST], url_path="adjust")
    def adjust_stock(self, request, pk=None, *args, **kwargs):
        """Adjust inventory quantity"""
        try:
            inventory = self.get_object()
            quantity = float(request.data.get('quantity', 0))
            adjustment_type = request.data.get('type', 'adjust')
            reason = request.data.get('reason', '')
            reference_number = request.data.get('reference_number', '')

            if quantity <= 0:
                return Response(
                    {'error': 'Quantity must be positive'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                # Create transaction record
                transaction_record = InventoryTransaction.objects.create(
                    inventory=inventory,
                    transaction_type=adjustment_type,
                    quantity=quantity if adjustment_type in ['in', 'add'] else -quantity,
                    reference_number=reference_number,
                    reason=reason,
                    created_by=request.user
                )

                # Update inventory quantity
                if adjustment_type in ['in', 'add']:
                    inventory.current_quantity += quantity
                elif adjustment_type in ['out', 'remove']:
                    inventory.current_quantity = max(0, inventory.current_quantity - quantity)
                elif adjustment_type == 'set':
                    inventory.current_quantity = quantity

                inventory.save()

            serializer = self.get_serializer(inventory)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=[Http.HTTP_GET], url_path="history")
    def get_history(self, request, pk=None, *args, **kwargs):
        """Get inventory transaction history"""
        try:
            inventory = self.get_object()
            transactions = inventory.transactions.all().order_by('-created_at')
            
            serializer = InventoryTransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=[Http.HTTP_GET, Http.HTTP_PUT, Http.HTTP_PATCH], url_path="config")
    def inventory_config(self, request, *args, **kwargs):
        """Get or update inventory configuration"""
        try:
            config = InventoryConfiguration.get_active_config()
            
            # Handle GET request
            if request.method == Http.HTTP_GET.upper():
                serializer = InventoryConfigurationSerializer(config)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # Handle PUT/PATCH request
            elif request.method in [Http.HTTP_PUT.upper(), Http.HTTP_PATCH.upper()]:
                serializer = InventoryConfigurationSerializer(
                    config, 
                    data=request.data, 
                    partial=(request.method == Http.HTTP_PATCH.upper())
                )
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
