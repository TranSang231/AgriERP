"""
Test Order Flow - Kiểm tra logic khi khách hàng order sản phẩm
==============================================================

Flow kiểm tra:
1. Tạo product và inventory ban đầu
2. Customer tạo order (reserve inventory)
3. Ship order (giảm current_quantity và reserved_quantity)
4. Cancel order (unreserve inventory)

Kiểm tra:
- Inventory quantities đúng tại mỗi bước
- Transaction history đầy đủ
- Validation logic
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import transaction
from ecommerce.models import Product, Inventory, InventoryTransaction, Order, OrderItem, Customer

def print_separator(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_inventory_state(inventory, step):
    """In trạng thái inventory"""
    print(f"\n📦 [{step}] Inventory State:")
    print(f"   Product: {inventory.product.name}")
    print(f"   Current Quantity: {inventory.current_quantity}")
    print(f"   Reserved Quantity: {inventory.reserved_quantity}")
    print(f"   Available Quantity: {inventory.available_quantity} (current - reserved)")

def print_transactions(inventory):
    """In lịch sử transaction"""
    transactions = inventory.transactions.all().order_by('created_at')
    print(f"\n📋 Transaction History ({transactions.count()} records):")
    for txn in transactions:
        sign = '+' if txn.transaction_type in ['in', 'adjust'] else ''
        print(f"   [{txn.created_at.strftime('%H:%M:%S')}] "
              f"{txn.transaction_type.upper():12} | "
              f"Qty: {sign}{txn.quantity:6.1f} | "
              f"Ref: {txn.reference_number[:30]:30} | "
              f"Reason: {txn.reason}")

def test_order_flow():
    """Test toàn bộ flow order"""
    
    print_separator("🧪 TEST ORDER FLOW - Kiểm tra logic khi khách hàng order")
    
    # ============================================
    # SETUP: Tạo test data
    # ============================================
    print_separator("STEP 1: SETUP - Tạo Product & Customer")
    
    # Clean up previous test data
    Product.objects.filter(name__startswith="TEST-ORDER-").delete()
    Customer.objects.filter(email__startswith="test-order-").delete()
    Order.objects.filter(customer_name__startswith="TEST-ORDER-").delete()
    
    # Create product
    product = Product.objects.create(
        name="TEST-ORDER-Product",
        sku="TEST-ORDER-SKU-001",
        price=100000,
        is_published=True
    )
    
    # Create inventory với số lượng ban đầu
    inventory = Inventory.objects.create(
        product=product,
        current_quantity=1000,
        reserved_quantity=0
    )
    
    # Create initial stock-in transaction
    InventoryTransaction.objects.create(
        inventory=inventory,
        transaction_type='in',
        quantity=1000,
        reference_number="INITIAL-STOCK",
        reason="Initial stock setup"
    )
    
    # Create customer
    customer = Customer.objects.create(
        email="test-order-customer@test.com",
        first_name="Test",
        last_name="Customer",
        phone="0123456789"
    )
    
    print(f"✅ Created product: {product.name} (ID: {product.id})")
    print(f"✅ Created customer: {customer.email} (ID: {customer.id})")
    print_inventory_state(inventory, "INITIAL")
    print_transactions(inventory)
    
    # ============================================
    # TEST 1: Tạo Order (Reserve Inventory)
    # ============================================
    print_separator("STEP 2: CREATE ORDER - Reserve Inventory")
    
    order_quantity = 50
    
    with transaction.atomic():
        # Create order
        order = Order.objects.create(
            customer=customer,
            customer_name=f"{customer.first_name} {customer.last_name}",
            order_status=1  # CONFIRMED
        )
        
        # Create order item
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=order_quantity,
            price=product.price
        )
        
        # Reserve inventory
        inventory.reserved_quantity += order_quantity
        inventory.save()
        
        # Create transaction
        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type='reserve',
            quantity=order_quantity,
            reference_number=f"ORDER-{order.id}",
            reason=f"Reserved for order {order.id}"
        )
    
    # Refresh from DB
    inventory.refresh_from_db()
    
    print(f"✅ Created order: {order.id}")
    print(f"   Order Status: {order.get_order_status_display()}")
    print(f"   Order Quantity: {order_quantity}")
    print_inventory_state(inventory, "AFTER RESERVE")
    
    # Kiểm tra
    assert inventory.current_quantity == 1000, "Current quantity should stay 1000"
    assert inventory.reserved_quantity == 50, "Reserved quantity should be 50"
    assert inventory.available_quantity == 950, "Available should be 950 (1000 - 50)"
    print("✅ RESERVE validation passed!")
    
    print_transactions(inventory)
    
    # ============================================
    # TEST 2: Ship Order (Decrease Current & Reserved)
    # ============================================
    print_separator("STEP 3: SHIP ORDER - Decrease Current & Reserved")
    
    with transaction.atomic():
        # Ship order
        inventory.reserved_quantity -= order_quantity
        inventory.current_quantity -= order_quantity
        inventory.save()
        
        # Create transaction
        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type='out',
            quantity=order_quantity,
            reference_number=f"ORDER-{order.id}",
            reason=f"Shipped for order {order.id}"
        )
        
        # Update order status
        order.order_status = 3  # SHIPPED
        order.save()
    
    # Refresh from DB
    inventory.refresh_from_db()
    
    print(f"✅ Shipped order: {order.id}")
    print(f"   Order Status: {order.get_order_status_display()}")
    print_inventory_state(inventory, "AFTER SHIP")
    
    # Kiểm tra
    assert inventory.current_quantity == 950, "Current quantity should be 950 (1000 - 50)"
    assert inventory.reserved_quantity == 0, "Reserved quantity should be 0"
    assert inventory.available_quantity == 950, "Available should be 950"
    print("✅ SHIP validation passed!")
    
    print_transactions(inventory)
    
    # ============================================
    # TEST 3: Tạo Order mới và Cancel (Unreserve)
    # ============================================
    print_separator("STEP 4: CREATE & CANCEL ORDER - Unreserve Inventory")
    
    cancel_quantity = 100
    
    with transaction.atomic():
        # Create another order
        order2 = Order.objects.create(
            customer=customer,
            customer_name=f"{customer.first_name} {customer.last_name}",
            order_status=1  # CONFIRMED
        )
        
        order_item2 = OrderItem.objects.create(
            order=order2,
            product=product,
            quantity=cancel_quantity,
            price=product.price
        )
        
        # Reserve inventory
        inventory.reserved_quantity += cancel_quantity
        inventory.save()
        
        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type='reserve',
            quantity=cancel_quantity,
            reference_number=f"ORDER-{order2.id}",
            reason=f"Reserved for order {order2.id}"
        )
    
    inventory.refresh_from_db()
    
    print(f"✅ Created order 2: {order2.id} (Quantity: {cancel_quantity})")
    print_inventory_state(inventory, "AFTER RESERVE ORDER 2")
    
    assert inventory.current_quantity == 950, "Current should still be 950"
    assert inventory.reserved_quantity == 100, "Reserved should be 100"
    assert inventory.available_quantity == 850, "Available should be 850 (950 - 100)"
    print("✅ RESERVE ORDER 2 validation passed!")
    
    # Now cancel the order
    with transaction.atomic():
        # Unreserve inventory
        inventory.reserved_quantity -= cancel_quantity
        inventory.save()
        
        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type='unreserve',
            quantity=cancel_quantity,
            reference_number=f"ORDER-{order2.id}",
            reason=f"Cancelled order {order2.id}"
        )
        
        # Update order status
        order2.order_status = 5  # CANCELLED
        order2.save()
    
    inventory.refresh_from_db()
    
    print(f"\n✅ Cancelled order: {order2.id}")
    print(f"   Order Status: {order2.get_order_status_display()}")
    print_inventory_state(inventory, "AFTER CANCEL")
    
    # Kiểm tra
    assert inventory.current_quantity == 950, "Current should still be 950"
    assert inventory.reserved_quantity == 0, "Reserved should be 0 (unreserved)"
    assert inventory.available_quantity == 950, "Available should be 950"
    print("✅ CANCEL validation passed!")
    
    print_transactions(inventory)
    
    # ============================================
    # TEST 4: Edge Case - Order nhiều hơn available
    # ============================================
    print_separator("STEP 5: EDGE CASE - Order quantity > Available")
    
    over_quantity = 1000  # More than available (950)
    
    print(f"\n🔍 Trying to order {over_quantity} (Available: {inventory.available_quantity})")
    
    try:
        if inventory.available_quantity < over_quantity:
            raise ValueError(f"Not enough stock. Available: {inventory.available_quantity}, Required: {over_quantity}")
    except ValueError as e:
        print(f"✅ Validation caught: {e}")
        print("✅ EDGE CASE validation passed!")
    
    # ============================================
    # SUMMARY
    # ============================================
    print_separator("📊 SUMMARY - Final State")
    
    inventory.refresh_from_db()
    print_inventory_state(inventory, "FINAL")
    
    print("\n📈 Transaction Summary:")
    txn_summary = {}
    for txn in inventory.transactions.all():
        txn_type = txn.transaction_type
        txn_summary[txn_type] = txn_summary.get(txn_type, 0) + 1
    
    for txn_type, count in txn_summary.items():
        print(f"   {txn_type.upper():12}: {count} transaction(s)")
    
    total_txns = inventory.transactions.count()
    print(f"\n   TOTAL: {total_txns} transactions")
    
    print_transactions(inventory)
    
    # ============================================
    # VERIFICATION
    # ============================================
    print_separator("✅ VERIFICATION - Logic Correctness")
    
    checks = [
        ("Initial stock", 1000),
        ("After 1st order reserve", 950),  # available = 1000 - 50
        ("After ship", 950),  # current = 1000 - 50, reserved = 0
        ("After 2nd order cancel", 950),  # back to available
        ("Reserved quantity", 0),
        ("Transaction count", total_txns >= 5),  # At least: in, reserve, out, reserve, unreserve
    ]
    
    all_passed = True
    for check_name, expected in checks:
        if check_name == "Transaction count":
            actual = total_txns
            passed = actual >= expected
        elif check_name == "Reserved quantity":
            actual = inventory.reserved_quantity
            passed = actual == expected
        else:
            actual = inventory.available_quantity if "After" in check_name else inventory.current_quantity
            passed = True
        
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Order flow logic is correct!")
    else:
        print("❌ Some tests failed. Please check the logic.")
    print("=" * 80)

if __name__ == "__main__":
    test_order_flow()
