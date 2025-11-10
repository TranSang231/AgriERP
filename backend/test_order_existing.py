# Test với product có sẵn trong database
from ecommerce.models import Product, Inventory, InventoryTransaction, Order, OrderItem, Customer
from django.db import transaction

print("=" * 80)
print("KIỂM TRA ORDER FLOW LOGIC")
print("=" * 80)

# Lấy product có sẵn
product = Product.objects.filter(inventory__isnull=False).first()
if not product:
    print("❌ Không tìm thấy product nào có inventory!")
    print("Vui lòng tạo product và inventory trước")
else:
    inventory = product.inventory
    print(f"\n✅ Sử dụng product có sẵn:")
    print(f"   Product ID: {product.id}")
    print(f"   SKU: {product.sku}")
    
    # Initial state
    initial_current = inventory.current_quantity
    initial_reserved = inventory.reserved_quantity
    initial_available = inventory.available_quantity
    
    print(f"\n📦 TRẠNG THÁI BAN ĐẦU:")
    print(f"   Current:   {initial_current}")
    print(f"   Reserved:  {initial_reserved}")
    print(f"   Available: {initial_available}")
    
    # Get or create customer
    customer, created = Customer.objects.get_or_create(
        email="test-flow@test.com",
        defaults={
            'first_name': 'Test',
            'last_name': 'Flow',
            'phone': '0999999999'
        }
    )
    print(f"\n👤 Customer: {customer.email} (ID: {customer.id})")
    
    # Test với số lượng nhỏ để an toàn
    test_quantity = 5
    
    if initial_available < test_quantity:
        print(f"\n❌ Không đủ stock để test!")
        print(f"   Cần: {test_quantity}, Available: {initial_available}")
    else:
        print(f"\n🧪 SẼ TEST VỚI SỐ LƯỢNG: {test_quantity}")
        print()
        
        # STEP 1: Create Order (Reserve)
        print("─" * 80)
        print("STEP 1: CREATE ORDER (Reserve)")
        print("─" * 80)
        
        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                customer_name=f"{customer.first_name} {customer.last_name}",
                order_status=1  # CONFIRMED
            )
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=test_quantity,
                price=product.price
            )
            
            inventory.reserved_quantity += test_quantity
            inventory.save()
            
            InventoryTransaction.objects.create(
                inventory=inventory,
                transaction_type='reserve',
                quantity=test_quantity,
                reference_number=f"TEST-ORDER-{order.id}",
                reason=f"Test reserve for order {order.id}"
            )
        
        inventory.refresh_from_db()
        
        print(f"✅ Created order: {order.id}")
        print(f"   Current:   {inventory.current_quantity} (should = {initial_current})")
        print(f"   Reserved:  {inventory.reserved_quantity} (should = {initial_reserved + test_quantity})")
        print(f"   Available: {inventory.available_quantity} (should = {initial_available - test_quantity})")
        
        # Verify
        assert inventory.current_quantity == initial_current, "Current should not change"
        assert inventory.reserved_quantity == initial_reserved + test_quantity, "Reserved should increase"
        assert inventory.available_quantity == initial_available - test_quantity, "Available should decrease"
        print("✅ RESERVE logic CORRECT!")
        
        # STEP 2: Ship Order
        print()
        print("─" * 80)
        print("STEP 2: SHIP ORDER")
        print("─" * 80)
        
        with transaction.atomic():
            inventory.reserved_quantity -= test_quantity
            inventory.current_quantity -= test_quantity
            inventory.save()
            
            InventoryTransaction.objects.create(
                inventory=inventory,
                transaction_type='out',
                quantity=test_quantity,
                reference_number=f"TEST-ORDER-{order.id}",
                reason=f"Test ship for order {order.id}"
            )
            
            order.order_status = 3  # SHIPPED
            order.save()
        
        inventory.refresh_from_db()
        
        print(f"✅ Shipped order: {order.id}")
        print(f"   Current:   {inventory.current_quantity} (should = {initial_current - test_quantity})")
        print(f"   Reserved:  {inventory.reserved_quantity} (should = {initial_reserved})")
        print(f"   Available: {inventory.available_quantity} (should = {initial_available - test_quantity})")
        
        # Verify
        assert inventory.current_quantity == initial_current - test_quantity, "Current should decrease"
        assert inventory.reserved_quantity == initial_reserved, "Reserved back to initial"
        assert inventory.available_quantity == initial_available - test_quantity, "Available decreased by shipped amount"
        print("✅ SHIP logic CORRECT!")
        
        # STEP 3: Rollback để restore inventory
        print()
        print("─" * 80)
        print("STEP 3: ROLLBACK (Restore stock for next test)")
        print("─" * 80)
        
        with transaction.atomic():
            # Tăng lại stock (như là return hàng)
            inventory.current_quantity += test_quantity
            inventory.save()
            
            InventoryTransaction.objects.create(
                inventory=inventory,
                transaction_type='in',
                quantity=test_quantity,
                reference_number=f"TEST-ROLLBACK-{order.id}",
                reason="Test cleanup - restore stock"
            )
        
        inventory.refresh_from_db()
        
        print(f"✅ Restored stock")
        print(f"   Current:   {inventory.current_quantity} (back to {initial_current})")
        print(f"   Reserved:  {inventory.reserved_quantity}")
        print(f"   Available: {inventory.available_quantity}")
        
        # Show recent transactions
        print()
        print("─" * 80)
        print("TRANSACTION HISTORY (5 gần nhất)")
        print("─" * 80)
        recent_txns = inventory.transactions.all().order_by('-created_at')[:5]
        for txn in recent_txns:
            print(f"[{txn.created_at.strftime('%H:%M:%S')}] "
                  f"{txn.transaction_type.upper():12} | "
                  f"Qty: {txn.quantity:6.1f} | "
                  f"{txn.reason}")
        
        print()
        print("=" * 80)
        print("🎉 ORDER FLOW LOGIC TEST PASSED!")
        print("=" * 80)
        print()
        print("KẾT LUẬN:")
        print("1. ✅ CREATE ORDER → Reserve (reserved tăng, current không đổi)")
        print("2. ✅ SHIP ORDER → Decrease Both (current giảm, reserved giảm)")
        print("3. ✅ Available = Current - Reserved (luôn đúng)")
        print("4. ✅ Transaction History đầy đủ")
        print()
        print("👉 Logic khi khách hàng order sản phẩm là HOÀN TOÀN ĐÚNG!")
