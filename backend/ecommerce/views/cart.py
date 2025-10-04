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
        customer_id = None
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                from django.core.cache import cache
                customer_id = cache.get(f'customer_token_{token}')
            except Exception:
                customer_id = None

        if not customer_id:
            try:
                customer_id = request.session.get('customer_id')
            except Exception:
                customer_id = None

        if customer_id:
            try:
                return Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                return None

        user = getattr(request, "user", None)
        if user and getattr(user, 'is_authenticated', False):
            return Customer.objects.filter(user=user).first()

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
        return super().retrieve(request, *args, **kwargs)

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
        item_id = kwargs.get("pk")
        item = get_object_or_404(CartItem, pk=item_id)
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
        item_id = kwargs.get("pk")
        item = get_object_or_404(CartItem, pk=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)