from base.views import BaseViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.core.cache import cache
from common.constants import Http
from ..models import Order, Inventory, InventoryTransaction, Product, Customer
from ..serializers import OrderSerializer
from ..constants.order_status import OrderStatus
from ..constants import PaymenStatus

class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    search_map = {
        "customer_first_name": "icontains",
        "customer_last_name": "icontains"
    }
    serializer_class = OrderSerializer
    # Require OAuth2/JWT via global DRF settings; keep class-level default
    permission_classes = [AllowAny]
    required_alternate_scopes = {
        "list": [],
        "retrieve": [],
        "create": [],
        "update": [["ecommerce:orders:edit-mine"]],
        "destroy": [["ecommerce:orders:edit-mine"]],
        "reserve_inventory": [["ecommerce:orders:edit-mine"]],
        "ship_order": [["ecommerce:orders:edit-mine"]],
        "cancel_order": [["ecommerce:orders:edit-mine"]]
    }

    def _get_current_customer(self, request):
        """Get current customer with proper authentication checks"""
        customer_id = None
        
        # Priority 1: Check Bearer token in Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                from django.core.cache import cache
                import hashlib
                token_hash = hashlib.sha256(token.encode()).hexdigest()
                cache_key = f'customer_token_{token_hash}'
                customer_id = cache.get(cache_key)
                
                if customer_id:
                    print(f"[ORDER] Found customer {customer_id} from token cache")
                else:
                    print(f"[ORDER] Token not found in cache or expired")
            except Exception as e:
                print(f"[ORDER] Error checking token cache: {e}")
                customer_id = None
        
        # Priority 2: Check session (fallback)
        if not customer_id:
            try:
                customer_id = request.session.get('customer_id')
                if customer_id:
                    print(f"[ORDER] Found customer {customer_id} from session")
            except Exception as e:
                print(f"[ORDER] Error checking session: {e}")
                customer_id = None
        
        # If we have customer_id, fetch the actual customer object
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
                print(f"[ORDER] Retrieved customer: {customer.id} ({customer.email})")
                return customer
            except Customer.DoesNotExist:
                print(f"[ORDER] Customer {customer_id} not found in database")
                return None
        
        # Priority 3: Check authenticated DRF user (for admin/staff)
        user = getattr(request, "user", None)
        if user and getattr(user, 'is_authenticated', False):
            user_id = getattr(user, 'id', None) or getattr(user, 'pk', None)
            if user_id:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    actual_user = User.objects.get(pk=user_id)
                    customer = Customer.objects.filter(user=actual_user).first()
                    if customer:
                        print(f"[ORDER] Found customer {customer.id} from DRF user")
                    return customer
                except User.DoesNotExist:
                    print(f"[ORDER] User {user_id} not found")
                    return None
        
        print(f"[ORDER] No customer found - not authenticated")
        return None

    def get_queryset(self):
        """Override to filter orders by current customer or allow admin access via OAuth scopes"""
        queryset = super().get_queryset()
        request = self.request
        user = getattr(request, 'user', None)
        
        # If user is Django staff/superuser, show all orders
        if user and getattr(user, 'is_staff', False):
            print(f"[ORDER QUERYSET] User is staff, returning all orders")
            return queryset
        
        # Check for admin OAuth scopes (for business app employees)
        if user and getattr(user, 'is_authenticated', False):
            # Try to get the access token from request
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                token_string = auth_header.split(' ')[1]
                try:
                    # Get the AccessToken object from django-oauth-toolkit
                    from oauth2_provider.models import get_access_token_model
                    AccessToken = get_access_token_model()
                    token_obj = AccessToken.objects.select_related('application').filter(token=token_string).first()
                    
                    if token_obj and token_obj.scope:
                        scopes = token_obj.scope.split()
                        print(f"[ORDER QUERYSET] Token scopes: {scopes}")
                        
                        # If user has admin scopes, show all orders
                        if any(scope in scopes for scope in ['ecommerce:orders:view', 'ecommerce:orders:edit']):
                            print(f"[ORDER QUERYSET] User has admin scopes, returning all orders")
                            return queryset
                except Exception as e:
                    print(f"[ORDER QUERYSET] Error checking token scopes: {e}")
        
        # For regular customers, only show their own orders
        customer = self._get_current_customer(request)
        if customer:
            print(f"[ORDER QUERYSET] Filtering by customer: {customer.id}")
            return queryset.filter(customer=customer)
        
        # If not authenticated, return empty queryset
        print(f"[ORDER QUERYSET] No customer found, returning empty queryset")
        return queryset.none()

    def list(self, request, *args, **kwargs):
        """List orders - filtered by get_queryset() based on user role"""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific order - ensure it belongs to current customer"""
        customer = self._get_current_customer(request)
        if not customer:
            return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        instance = self.get_object()
        
        # Verify the order belongs to the current customer (unless admin)
        user = getattr(request, 'user', None)
        if not (user and getattr(user, 'is_staff', False)):
            if instance.customer != customer:
                return Response(
                    {"detail": "You don't have permission to view this order"},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create order and reserve inventory"""
        # Idempotency: prevent duplicate submissions
        idempotency_key = request.headers.get('Idempotency-Key') or request.META.get('HTTP_IDEMPOTENCY_KEY')
        if idempotency_key:
            cache_key = f"order:create:{idempotency_key}"
            cached_response = cache.get(cache_key)
            if cached_response:
                return Response(cached_response, status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Recalculate monetary fields server-side (basic; extend with promotions as needed)
        # Note: OrderItem.save computes amount = price * quantity; this ensures consistency

        # Resolve authenticated customer via token/session
        # Use the existing _get_current_customer method which properly handles all auth scenarios
        customer = self._get_current_customer(request)
        if not customer:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # First validate all items before creating the order
        items_to_reserve = []
        for item_data in request.data.get('items', []):
            # Validate each item has required fields
            product_id = item_data.get('product') or item_data.get('product_id')
            if not product_id:
                return Response(
                    {'error': 'All order items must have a product specified'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                product = Product.objects.get(id=product_id)
                quantity = float(item_data.get('quantity', 0))
                
                # Check if product exists
                if not product:
                    return Response(
                        {'error': f'Product with ID {product_id} not found'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Check if product has inventory
                if not hasattr(product, 'inventory'):
                    return Response(
                        {'error': f'Product {product_id} does not have inventory configured'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                inventory = product.inventory
                if not inventory:
                    return Response(
                        {'error': f'Inventory not found for product {product_id}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Check if enough inventory available (current - reserved)
                if inventory.available_quantity < quantity:
                    return Response(
                        {'error': f'Not enough stock for product {product_id}. Available: {inventory.available_quantity}, Required: {quantity}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                items_to_reserve.append((inventory, quantity))
                
            except Product.DoesNotExist:
                return Response(
                    {'error': f'Product with ID {product_id} does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except (ValueError, TypeError) as e:
                return Response(
                    {'error': f'Invalid quantity specified: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': f'Error validating product {product_id}: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        # All items validated, now create the order and reserve inventory
        with transaction.atomic():
            # Create the order
            order = serializer.save(customer=customer)
            # Ensure payment status reflects COD (unpaid yet)
            if order.payment_status != PaymenStatus.INITIATED:
                order.payment_status = PaymenStatus.INITIATED
            # Confirm the order after reservation
            order.order_status = OrderStatus.CONFIRMED
            order.save()
            
            # Reserve inventory for each validated item
            for inventory, quantity in items_to_reserve:
                try:
                    # Reserve inventory
                    inventory.reserved_quantity += quantity
                    inventory.save()
                    
                    # Create transaction record
                    InventoryTransaction.objects.create(
                        inventory=inventory,
                        transaction_type='reserve',
                        quantity=quantity,
                        reference_number=f"ORDER-{order.id}",
                        reason=f"Reserved for order {order.id}",
                        created_by=request.user if request.user.is_authenticated else None
                    )
                except Exception as e:
                    # Rollback will happen automatically due to transaction.atomic()
                    return Response(
                        {'error': f'Failed to reserve inventory: {str(e)}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
        
        response_data = serializer.data
        if idempotency_key:
            cache_key = f"order:create:{idempotency_key}"
            cache.set(cache_key, response_data, timeout=60 * 10)  # 10 minutes
        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=[Http.HTTP_POST], url_path="ship")
    def ship_order(self, request, pk=None):
        """Ship order and update inventory"""
        # Verify customer ownership (unless admin)
        customer = self._get_current_customer(request)
        user = getattr(request, 'user', None)
        is_staff = user and getattr(user, 'is_staff', False)
        
        order = self.get_object()
        
        if not is_staff:
            if not customer:
                return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            if order.customer != customer:
                return Response(
                    {"detail": "You don't have permission to ship this order"},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        if order.order_status not in [OrderStatus.CONFIRMED, OrderStatus.PROCESSING]:
            return Response(
                {'error': 'Order must be confirmed or processing to ship'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            errors = []
            for item in order.items.all():
                if item.product:
                    try:
                        # Check if product has inventory
                        if not hasattr(item.product, 'inventory') or not item.product.inventory:
                            errors.append(f"Product {item.product.id} has no inventory configured")
                            continue  # Skip if no inventory
                        
                        inventory = item.product.inventory
                        quantity = item.quantity
                        
                        # Check if reserved quantity is sufficient
                        if inventory.reserved_quantity < quantity:
                            errors.append(f"Insufficient reserved quantity for product {item.product.id}")
                            continue
                        
                        # Move from reserved to out
                        inventory.reserved_quantity -= quantity
                        inventory.current_quantity -= quantity
                        inventory.save()
                        
                        # Create transaction record
                        InventoryTransaction.objects.create(
                            inventory=inventory,
                            transaction_type='out',
                            quantity=quantity,
                            reference_number=f"ORDER-{order.id}",
                            reason=f"Shipped for order {order.id}",
                            created_by=request.user if request.user.is_authenticated else None
                        )
                        
                    except Exception as e:
                        errors.append(f"Error processing product {item.product.id}: {str(e)}")
                        continue
            
            if errors and len(errors) == len(list(order.items.all())):
                # All items failed
                return Response(
                    {'error': f'Failed to ship order: {"; ".join(errors)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif errors:
                # Some items failed, but process continues
                # Optionally log these errors
                pass
            
            # Update order status
            order.order_status = OrderStatus.SHIPPED
            order.save()
        
        return Response({'status': 'Order shipped successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=[Http.HTTP_POST], url_path="cancel")
    def cancel_order(self, request, pk=None):
        """Cancel order and unreserve inventory"""
        # Verify customer ownership (unless admin)
        customer = self._get_current_customer(request)
        user = getattr(request, 'user', None)
        is_staff = user and getattr(user, 'is_staff', False)
        
        order = self.get_object()
        
        if not is_staff:
            if not customer:
                return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            if order.customer != customer:
                return Response(
                    {"detail": "You don't have permission to cancel this order"},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        if order.order_status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            return Response(
                {'error': 'Cannot cancel shipped or delivered orders'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            errors = []
            for item in order.items.all():
                if item.product:
                    try:
                        # Check if product has inventory
                        if not hasattr(item.product, 'inventory') or not item.product.inventory:
                            errors.append(f"Product {item.product.id} has no inventory configured")
                            continue  # Skip if no inventory
                        
                        inventory = item.product.inventory
                        quantity = item.quantity
                        
                        # Check if we can unreserve (make sure reserved quantity is enough)
                        if inventory.reserved_quantity < quantity:
                            # Still continue with unreserve but update the quantity to match reserved
                            quantity = min(quantity, inventory.reserved_quantity)
                            errors.append(f"Adjusted unreserve quantity for product {item.product.id}")
                        
                        # Unreserve inventory
                        inventory.reserved_quantity = max(0, inventory.reserved_quantity - quantity)
                        inventory.save()
                        
                        # Create transaction record
                        InventoryTransaction.objects.create(
                            inventory=inventory,
                            transaction_type='unreserve',
                            quantity=quantity,
                            reference_number=f"ORDER-{order.id}",
                            reason=f"Cancelled order {order.id}",
                            created_by=request.user if request.user.is_authenticated else None
                        )
                        
                    except Exception as e:
                        errors.append(f"Error processing product {item.product.id}: {str(e)}")
                        continue
            
            # Update order status (even if there were errors)
            order.order_status = OrderStatus.CANCELLED
            order.save()
        
        if errors:
            return Response(
                {'status': 'Order cancelled with warnings', 'warnings': errors},
                status=status.HTTP_200_OK
            )
        
        return Response({'status': 'Order cancelled successfully'}, status=status.HTTP_200_OK)