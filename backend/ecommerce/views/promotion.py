from base.views import BaseViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from ..models import Promotion, PromotionItem
from ..serializers import PromotionSerializer


class PromotionViewSet(BaseViewSet):
    queryset = Promotion.objects.all()
    search_map = {
        "name__ogigin": "icontains",
        "description__ogigin": "icontains"
    }
    serializer_class = PromotionSerializer
    # Allow public access to promotions (no auth required)
    permission_classes = [AllowAny]
    required_alternate_scopes = {
        "list": [],
        "retrieve": [],
        "create": [["ecommerce:promotions:edit"]],
        "update": [["ecommerce:promotions:edit"]],
        "destroy": [["ecommerce:promotions:edit"]]
    }

    def list(self, request, *args, **kwargs):
        """Override list to handle date filtering for active promotions"""
        queryset = self.get_queryset()
        
        # Check for date filtering parameters
        start_lte = request.query_params.get('start__lte')
        end_gte = request.query_params.get('end__gte')
        
        if start_lte and end_gte:
            # Filter for active promotions
            from django.utils import timezone
            from django.db.models import Q
            
            try:
                start_date = timezone.datetime.fromisoformat(start_lte.replace('Z', '+00:00'))
                end_date = timezone.datetime.fromisoformat(end_gte.replace('Z', '+00:00'))
                
                # Find promotions that are active between these dates
                queryset = queryset.filter(
                    Q(start__lte=end_date) & Q(end__gte=start_date)
                )
            except (ValueError, TypeError):
                # If date parsing fails, return all promotions
                pass
        
        # Apply other filters
        queryset = self.filter_queryset(queryset)
        
        # Handle pagination
        page_size = request.query_params.get('page_size')
        if page_size:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='validate', permission_classes=[AllowAny])
    def validate_promotion(self, request):
        """Validate if a promotion can be applied to given products and quantities"""
        promotion_id = request.data.get('promotion_id')
        product_ids = request.data.get('product_ids', [])
        quantities = request.data.get('quantities', [])
        
        if not promotion_id or not product_ids:
            return Response({
                'valid': False,
                'message': 'Promotion ID and product IDs are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            promotion = Promotion.objects.get(id=promotion_id)
            
            # Check if promotion is active
            now = timezone.now()
            if promotion.start > now or promotion.end < now:
                return Response({
                    'valid': False,
                    'message': 'Promotion is not active'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Calculate total discount
            total_discount = 0
            from ..models import Product
            if getattr(promotion, 'type', 'discount') == getattr(Promotion, 'TYPE_VOUCHER', 'voucher'):
                # Voucher: apply promotion.discount to all selected products
                for i, product_id in enumerate(product_ids):
                    try:
                        product = Product.objects.get(id=product_id)
                        quantity = quantities[i] if i < len(quantities) else 1
                        product_price = getattr(product, 'sale_price', None) or getattr(product, 'price', 0) or 0
                        item_discount = (float(getattr(promotion, 'discount', 0)) / 100.0) * float(product_price) * float(quantity)
                        total_discount += item_discount
                    except Product.DoesNotExist:
                        continue
            else:
                # Discount: product-level via PromotionItem
                for i, product_id in enumerate(product_ids):
                    try:
                        promotion_item = PromotionItem.objects.get(
                            promotion=promotion,
                            product_id=product_id
                        )
                        quantity = quantities[i] if i < len(quantities) else 1
                        
                        # Check quantity limits
                        if promotion_item.quantity_limit > 0 and quantity > promotion_item.quantity_limit:
                            return Response({
                                'valid': False,
                                'message': f'Quantity exceeds limit for product {product_id}'
                            }, status=status.HTTP_400_BAD_REQUEST)
                        
                        product = Product.objects.get(id=product_id)
                        product_price = getattr(product, 'sale_price', None) or getattr(product, 'price', 0) or 0
                        
                        # Calculate discount for this item: (discount_percent / 100) * price * quantity
                        item_discount = (promotion_item.discount / 100) * float(product_price) * float(quantity)
                        total_discount += item_discount
                        
                    except PromotionItem.DoesNotExist:
                        continue
                    except Product.DoesNotExist:
                        continue
            
            return Response({
                'valid': True,
                'discount': total_discount
            }, status=status.HTTP_200_OK)
            
        except Promotion.DoesNotExist:
            return Response({
                'valid': False,
                'message': 'Promotion not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'valid': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)