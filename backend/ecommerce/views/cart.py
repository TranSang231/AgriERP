from base.views import BaseViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from ..models import Cart, CartItem, Product, Customer
from ..serializers import CartSerializer
from ..serializers.cart_item import CartItemSerializer

class CartViewSet(BaseViewSet):
    queryset = Cart.objects.all()
    search_map = {
        "customer__first_name": "icontains",
        "customer__last_name": "icontains"
    }
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    required_alternate_scopes = {}

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
                    print(f"[CART] Found customer {customer_id} from token cache")
                else:
                    print(f"[CART] Token not found in cache or expired")
            except Exception as e:
                print(f"[CART] Error checking token cache: {e}")
                customer_id = None

        # Priority 2: Check session (fallback)
        if not customer_id:
            try:
                customer_id = request.session.get('customer_id')
                if customer_id:
                    print(f"[CART] Found customer {customer_id} from session")
            except Exception as e:
                print(f"[CART] Error checking session: {e}")
                customer_id = None

        # If we have customer_id, fetch the actual customer object
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
                print(f"[CART] Retrieved customer: {customer.id} ({customer.email})")
                return customer
            except Customer.DoesNotExist:
                print(f"[CART] Customer {customer_id} not found in database")
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
                        print(f"[CART] Found customer {customer.id} from DRF user")
                    return customer
                except User.DoesNotExist:
                    print(f"[CART] User {user_id} not found")
                    return None

        print(f"[CART] No customer found - not authenticated")
        return None

    def _get_or_create_cart(self, customer):
        if customer is None:
            return None
        cart, _ = Cart.objects.get_or_create(customer=customer)
        return cart

    def list(self, request, *args, **kwargs):
        customer = self._get_current_customer(request)
        cart = self._get_or_create_cart(customer)
        if cart is None:
            data = CartSerializer(instance=Cart(), context=self.get_serializer_context()).data
            data.update({"items": []})
            return Response(data, status=status.HTTP_200_OK)
        serializer = CartSerializer(instance=cart, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific cart by ID - ensure it belongs to current customer"""
        customer = self._get_current_customer(request)
        if customer is None:
            return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        cart_id = kwargs.get("pk")
        cart = get_object_or_404(Cart, pk=cart_id)
        
        # Verify that the cart belongs to the current customer
        if cart.customer != customer:
            return Response({"detail": "You don't have permission to view this cart"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CartSerializer(instance=cart, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Add an item to the current customer's cart.

        Expected payload: { "product_id": number, "quantity": number }
        Returns: CartItem serialized
        """
        customer = self._get_current_customer(request)
        cart = self._get_or_create_cart(customer)
        if cart is None:
            return Response({"detail": "Customer not found."}, status=status.HTTP_400_BAD_REQUEST)

        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)
        if not product_id:
            return Response({"detail": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity = float(quantity)
            if quantity <= 0:
                raise ValueError()
        except Exception:
            return Response({"detail": "quantity must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id)

        origin_price = getattr(product, "sale_price", None)
        if origin_price is None:
            origin_price = getattr(product, "price", 0) or 0
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "quantity": quantity,
                "origin_price": origin_price,
                "selected": True,
            },
        )
        if not created:
            item.quantity = (item.quantity or 0) + quantity
            item.save(update_fields=["quantity", "updated_at"])

        serializer = CartItemSerializer(instance=item, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Treat pk as CartItem id and update its quantity."""
        customer = self._get_current_customer(request)
        if customer is None:
            return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        item_id = kwargs.get("pk")
        item = get_object_or_404(CartItem, pk=item_id)
        
        # Verify that the cart item belongs to the current customer
        if item.cart.customer != customer:
            return Response({"detail": "You don't have permission to modify this cart item"}, status=status.HTTP_403_FORBIDDEN)
        
        quantity = request.data.get("quantity")
        if quantity is None:
            return Response({"detail": "quantity is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity = float(quantity)
            if quantity <= 0:
                raise ValueError()
        except Exception:
            return Response({"detail": "quantity must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)
        item.quantity = quantity
        item.save(update_fields=["quantity", "updated_at"])
        serializer = CartItemSerializer(instance=item, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Treat pk as CartItem id and delete it."""
        customer = self._get_current_customer(request)
        if customer is None:
            return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        item_id = kwargs.get("pk")
        item = get_object_or_404(CartItem, pk=item_id)
        
        # Verify that the cart item belongs to the current customer
        if item.cart.customer != customer:
            return Response({"detail": "You don't have permission to delete this cart item"}, status=status.HTTP_403_FORBIDDEN)
        
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)