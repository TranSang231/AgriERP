import logging
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import get_user_model

from base.views import BaseViewSet
from common.constants import Http
from ..models import GoodsReceipt, Product, Inventory, InventoryTransaction
from ..serializers import GoodsReceiptSerializer

User = get_user_model()


log = logging.getLogger("ecommerce.goods_receipts")


class GoodsReceiptViewSet(BaseViewSet):
    queryset = GoodsReceipt.objects.prefetch_related(
        'items',
        'items__product',
        'items__product__name',
        'items__unit'
    ).all()
    search_map = {
        "supplier_name": "icontains",
        "reference_code": "icontains",
        "note": "icontains",
    }
    serializer_class = GoodsReceiptSerializer
    required_alternate_scopes = {
        "list": [
            ["ecommerce:goods-receipts:view"],
            ["ecommerce:goods-receipts:edit"],
            ["ecommerce:orders:view"],
            ["ecommerce:orders:edit"],
        ],
        "retrieve": [
            ["ecommerce:goods-receipts:view"],
            ["ecommerce:goods-receipts:edit"],
            ["ecommerce:orders:view"],
            ["ecommerce:orders:edit"],
        ],
        "create": [["ecommerce:goods-receipts:edit"], ["ecommerce:orders:edit"]],
        "update": [["ecommerce:goods-receipts:edit"], ["ecommerce:orders:edit"]],
        "destroy": [["ecommerce:goods-receipts:edit"], ["ecommerce:orders:edit"]],
        "apply": [["ecommerce:goods-receipts:edit"], ["ecommerce:orders:edit"]],
        "unapply": [["ecommerce:goods-receipts:edit"], ["ecommerce:orders:edit"]],
    }

    def create(self, request, *args, **kwargs):
        try:
            log.debug("[GoodsReceipt.create] payload=%s", request.data)
            print(f"[GOODS RECEIPT CREATE] Request data: {request.data}")
        except Exception as e:
            print(f"[GOODS RECEIPT CREATE] Error logging request: {e}")
        
        # Validate serializer explicitly
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(f"[GOODS RECEIPT CREATE] Validation errors: {serializer.errors}")
            log.error("[GoodsReceipt.create] validation_errors=%s", serializer.errors)
            return Response(serializer.errors, status=400)
        
        try:
            # Save the instance
            self.perform_create(serializer)
            
            # Refresh from DB to get related items
            instance = GoodsReceipt.objects.prefetch_related(
                'items',
                'items__product',
                'items__product__name',
                'items__unit'
            ).get(pk=serializer.instance.pk)
            
            # Re-serialize with full context
            response_serializer = self.get_serializer(instance)
            
            try:
                log.debug("[GoodsReceipt.create] response=%s", response_serializer.data)
                print(f"[GOODS RECEIPT CREATE] Response data: {response_serializer.data}")
            except Exception:
                pass
            
            return Response(response_serializer.data, status=201)
        except Exception as e:
            print(f"[GOODS RECEIPT CREATE] Error: {e}")
            import traceback
            print(traceback.format_exc())
            raise

    def update(self, request, *args, **kwargs):
        try:
            log.debug("[GoodsReceipt.update] id=%s payload=%s", kwargs.get('pk'), request.data)
        except Exception:
            pass
        
        # Get partial flag
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # ✅ PREVENT UPDATING APPLIED RECEIPTS
        if instance.is_applied:
            return Response(
                {"detail": "Cannot update an already applied goods receipt. Please unapply it first or create a new one."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Serialize and validate
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Refresh from DB with relations
        instance = GoodsReceipt.objects.prefetch_related(
            'items',
            'items__product',
            'items__product__name',
            'items__unit'
        ).get(pk=instance.pk)
        
        # Re-serialize with full context
        response_serializer = self.get_serializer(instance)
        
        try:
            log.debug("[GoodsReceipt.update] id=%s response=%s", kwargs.get('pk'), response_serializer.data)
        except Exception:
            pass
        
        return Response(response_serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a goods receipt.
        ✅ IMPORTANT: Cannot delete applied goods receipts to prevent stock corruption.
        """
        instance = self.get_object()
        
        # ✅ PREVENT DELETING APPLIED RECEIPTS
        if instance.is_applied:
            return Response(
                {
                    "detail": "Cannot delete an already applied goods receipt. "
                              "This would corrupt inventory data. "
                              "Please unapply it first or contact administrator."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete if not applied
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=[Http.HTTP_POST], url_path="apply")
    def apply(self, request, *args, **kwargs):
        receipt: GoodsReceipt = self.get_object()
        if receipt.is_applied:
            return Response({"detail": "Receipt already applied"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the actual User instance from request.user
        user_instance = None
        if request.user and request.user.is_authenticated:
            try:
                # request.user might be a JWTUser, get the actual User model instance
                user_instance = User.objects.get(pk=request.user.id)
            except User.DoesNotExist:
                user_instance = None

        with transaction.atomic():
            items = receipt.items.select_related("product").all()
            for item in items:
                product: Product = item.product
                # Convert Decimal to float for calculation
                quantity = float(item.quantity or 0.0)
                
                # ✅ USE HELPER METHOD - No need to update Product.in_stock manually
                # add_stock() will update Inventory.current_quantity and create transaction log
                product.add_stock(
                    quantity=quantity,
                    reason=receipt.note or "Goods receipt applied",
                    reference_number=f"GR-{receipt.id}",
                    user=user_instance
                )

        receipt.mark_applied()

        serializer = self.get_serializer(receipt)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=[Http.HTTP_POST], url_path="unapply")
    def unapply(self, request, *args, **kwargs):
        """
        Unapply (revert) a goods receipt.
        This will reverse the stock changes made when the receipt was applied.
        """
        receipt: GoodsReceipt = self.get_object()
        
        # ✅ CHECK IF ALREADY UNAPPLIED
        if not receipt.is_applied:
            return Response(
                {"detail": "Receipt is not applied yet. Nothing to unapply."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the actual User instance from request.user
        user_instance = None
        if request.user and request.user.is_authenticated:
            try:
                user_instance = User.objects.get(pk=request.user.id)
            except User.DoesNotExist:
                user_instance = None

        with transaction.atomic():
            items = receipt.items.select_related("product").all()
            for item in items:
                product: Product = item.product
                # Convert Decimal to float for calculation
                quantity = float(item.quantity or 0.0)
                
                # ✅ REDUCE STOCK - Reverse the apply operation
                product.reduce_stock(
                    quantity=quantity,
                    reason=f"Unapply goods receipt: {receipt.note or 'No note'}",
                    reference_number=f"GR-UNAPPLY-{receipt.id}",
                    user=user_instance
                )

            # ✅ MARK AS UNAPPLIED
            receipt.is_applied = False
            receipt.applied_at = None
            receipt.save(update_fields=["is_applied", "applied_at", "updated_at"])

        serializer = self.get_serializer(receipt)
        return Response(serializer.data, status=status.HTTP_200_OK)




