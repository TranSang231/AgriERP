"""
Test script for Goods Receipt Unapply functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from decimal import Decimal
from django.contrib.auth import get_user_model
from ecommerce.models import (
    GoodsReceipt, 
    GoodsReceiptItem, 
    Product, 
    Inventory,
    InventoryTransaction
)

User = get_user_model()

def test_unapply_logic():
    """
    Test the unapply logic without making actual HTTP requests.
    This simulates what the API endpoint does.
    """
    print("=" * 80)
    print("TESTING GOODS RECEIPT UNAPPLY LOGIC")
    print("=" * 80)
    
    # Find a product with inventory
    product = Product.objects.select_related('inventory').filter(
        inventory__isnull=False
    ).first()
    
    if not product:
        print("❌ No product with inventory found!")
        return
    
    print(f"\n📦 Testing with Product: {product.name}")
    print(f"   Initial Stock: {product.in_stock}")
    
    # Get or create a test user
    user = User.objects.filter(is_superuser=True).first()
    print(f"👤 User: {user.username if user else 'None'}")
    
    # Find an applied goods receipt or create one
    receipt = GoodsReceipt.objects.filter(is_applied=False).first()
    
    if not receipt:
        print("\n⚠️  No unapplied receipt found. Creating test receipt...")
        receipt = GoodsReceipt.objects.create(
            supplier_name="Test Supplier",
            reference_code="TEST-001",
            note="Test receipt for unapply",
            created_by=user
        )
        
        # Add item
        GoodsReceiptItem.objects.create(
            receipt=receipt,
            product=product,
            quantity=Decimal("50.00"),
            unit_cost=Decimal("100.00"),
            unit=product.unit
        )
        print(f"✅ Created test receipt #{receipt.id}")
    
    print(f"\n📄 Receipt #{receipt.id}")
    print(f"   Status: {'Applied' if receipt.is_applied else 'Not Applied'}")
    print(f"   Items: {receipt.items.count()}")
    
    # Test 1: Apply Receipt
    print("\n" + "=" * 80)
    print("TEST 1: APPLY RECEIPT")
    print("=" * 80)
    
    if not receipt.is_applied:
        initial_stock = product.in_stock
        print(f"Before Apply - Stock: {initial_stock}")
        
        # Simulate apply action
        items = receipt.items.select_related("product").all()
        for item in items:
            quantity = float(item.quantity or 0.0)
            print(f"  Adding {quantity} units to {item.product.name}")
            item.product.add_stock(
                quantity=quantity,
                reason=f"Apply receipt {receipt.id}",
                reference_number=f"GR-{receipt.id}",
                user=user
            )
        
        receipt.mark_applied()
        
        # Refresh product
        product.refresh_from_db()
        product.inventory.refresh_from_db()
        
        final_stock = product.in_stock
        print(f"After Apply  - Stock: {final_stock}")
        print(f"✅ Stock increased by {final_stock - initial_stock}")
    else:
        print("⚠️  Receipt already applied")
    
    # Test 2: Unapply Receipt
    print("\n" + "=" * 80)
    print("TEST 2: UNAPPLY RECEIPT")
    print("=" * 80)
    
    if receipt.is_applied:
        initial_stock = product.in_stock
        print(f"Before Unapply - Stock: {initial_stock}")
        
        # Simulate unapply action
        items = receipt.items.select_related("product").all()
        for item in items:
            quantity = float(item.quantity or 0.0)
            print(f"  Reducing {quantity} units from {item.product.name}")
            item.product.reduce_stock(
                quantity=quantity,
                reason=f"Unapply receipt {receipt.id}",
                reference_number=f"GR-UNAPPLY-{receipt.id}",
                user=user
            )
        
        # Mark as unapplied
        receipt.is_applied = False
        receipt.applied_at = None
        receipt.save(update_fields=["is_applied", "applied_at", "updated_at"])
        
        # Refresh product
        product.refresh_from_db()
        product.inventory.refresh_from_db()
        
        final_stock = product.in_stock
        print(f"After Unapply  - Stock: {final_stock}")
        print(f"✅ Stock decreased by {initial_stock - final_stock}")
    else:
        print("⚠️  Receipt is not applied")
    
    # Test 3: Check Inventory Transactions
    print("\n" + "=" * 80)
    print("TEST 3: INVENTORY TRANSACTIONS AUDIT TRAIL")
    print("=" * 80)
    
    transactions = InventoryTransaction.objects.filter(
        reference_number__contains=f"GR-{receipt.id}"
    ).order_by('-created_at')[:5]
    
    print(f"\nRecent transactions for GR-{receipt.id}:")
    for txn in transactions:
        print(f"  {txn.created_at.strftime('%Y-%m-%d %H:%M:%S')} | "
              f"{txn.type:8} | {txn.quantity:8.2f} | "
              f"{txn.reference_number:20} | {txn.reason}")
    
    # Final status
    print("\n" + "=" * 80)
    print("FINAL STATUS")
    print("=" * 80)
    print(f"Receipt #{receipt.id}: {'Applied' if receipt.is_applied else 'Unapplied'}")
    print(f"Product Stock: {product.in_stock}")
    print(f"Inventory Transactions: {InventoryTransaction.objects.filter(inventory=product.inventory).count()}")
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_unapply_logic()
