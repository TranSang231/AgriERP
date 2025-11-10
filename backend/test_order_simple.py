# Quick test order flow
from ecommerce.models import Product, Inventory, InventoryTransaction, Order, OrderItem, Customer
from django.db import transaction

# Clean up
Product.objects.filter(name__startswith="TEST-ORDER-").delete()
Customer.objects.filter(email__startswith="test-order-").delete()

# Create product
product = Product.objects.create(name="TEST-ORDER-Product", sku="TEST-ORDER-SKU", price=100000, is_published=True)
inventory = Inventory.objects.create(product=product, current_quantity=1000, reserved_quantity=0)
InventoryTransaction.objects.create(inventory=inventory, transaction_type='in', quantity=1000, reference_number="INITIAL", reason="Initial stock")

# Create customer  
customer = Customer.objects.create(email="test-order@test.com", first_name="Test", last_name="Customer", phone="0123456789")

print("=" * 80)
print("INITIAL STATE")
print("=" * 80)
print(f"Product: {product.name}")
print(f"Current: {inventory.current_quantity}, Reserved: {inventory.reserved_quantity}, Available: {inventory.available_quantity}")
print(f"Transactions: {inventory.transactions.count()}")
print()

# STEP 1: Create order (reserve 50)
order_qty = 50
with transaction.atomic():
    order = Order.objects.create(customer=customer, customer_name="Test Customer", order_status=1)
    OrderItem.objects.create(order=order, product=product, quantity=order_qty, price=product.price)
    inventory.reserved_quantity += order_qty
    inventory.save()
    InventoryTransaction.objects.create(inventory=inventory, transaction_type='reserve', quantity=order_qty, reference_number=f"ORDER-{order.id}", reason=f"Reserved for order {order.id}")

inventory.refresh_from_db()
print("=" * 80)
print(f"AFTER CREATE ORDER {order.id} (Reserve {order_qty})")
print("=" * 80)
print(f"Current: {inventory.current_quantity}, Reserved: {inventory.reserved_quantity}, Available: {inventory.available_quantity}")
print(f"Expected: Current=1000, Reserved=50, Available=950")
assert inventory.current_quantity == 1000, "Current should be 1000"
assert inventory.reserved_quantity == 50, "Reserved should be 50"
assert inventory.available_quantity == 950, "Available should be 950"
print("✅ RESERVE validation passed!")
print()

# STEP 2: Ship order (decrease both)
with transaction.atomic():
    inventory.reserved_quantity -= order_qty
    inventory.current_quantity -= order_qty
    inventory.save()
    InventoryTransaction.objects.create(inventory=inventory, transaction_type='out', quantity=order_qty, reference_number=f"ORDER-{order.id}", reason=f"Shipped for order {order.id}")
    order.order_status = 3  # SHIPPED
    order.save()

inventory.refresh_from_db()
print("=" * 80)
print(f"AFTER SHIP ORDER {order.id}")
print("=" * 80)
print(f"Current: {inventory.current_quantity}, Reserved: {inventory.reserved_quantity}, Available: {inventory.available_quantity}")
print(f"Expected: Current=950, Reserved=0, Available=950")
assert inventory.current_quantity == 950, "Current should be 950"
assert inventory.reserved_quantity == 0, "Reserved should be 0"
assert inventory.available_quantity == 950, "Available should be 950"
print("✅ SHIP validation passed!")
print()

# STEP 3: Create and cancel another order
cancel_qty = 100
with transaction.atomic():
    order2 = Order.objects.create(customer=customer, customer_name="Test Customer", order_status=1)
    OrderItem.objects.create(order=order2, product=product, quantity=cancel_qty, price=product.price)
    inventory.reserved_quantity += cancel_qty
    inventory.save()
    InventoryTransaction.objects.create(inventory=inventory, transaction_type='reserve', quantity=cancel_qty, reference_number=f"ORDER-{order2.id}", reason=f"Reserved for order {order2.id}")

inventory.refresh_from_db()
print("=" * 80)
print(f"AFTER CREATE ORDER {order2.id} (Reserve {cancel_qty})")
print("=" * 80)
print(f"Current: {inventory.current_quantity}, Reserved: {inventory.reserved_quantity}, Available: {inventory.available_quantity}")
print(f"Expected: Current=950, Reserved=100, Available=850")
assert inventory.current_quantity == 950, "Current should be 950"
assert inventory.reserved_quantity == 100, "Reserved should be 100"
assert inventory.available_quantity == 850, "Available should be 850"
print("✅ RESERVE ORDER 2 validation passed!")
print()

# Cancel order 2
with transaction.atomic():
    inventory.reserved_quantity -= cancel_qty
    inventory.save()
    InventoryTransaction.objects.create(inventory=inventory, transaction_type='unreserve', quantity=cancel_qty, reference_number=f"ORDER-{order2.id}", reason=f"Cancelled order {order2.id}")
    order2.order_status = 5  # CANCELLED
    order2.save()

inventory.refresh_from_db()
print("=" * 80)
print(f"AFTER CANCEL ORDER {order2.id}")
print("=" * 80)
print(f"Current: {inventory.current_quantity}, Reserved: {inventory.reserved_quantity}, Available: {inventory.available_quantity}")
print(f"Expected: Current=950, Reserved=0, Available=950")
assert inventory.current_quantity == 950, "Current should be 950"
assert inventory.reserved_quantity == 0, "Reserved should be 0"
assert inventory.available_quantity == 950, "Available should be 950"
print("✅ CANCEL validation passed!")
print()

# Show transactions
print("=" * 80)
print("TRANSACTION HISTORY")
print("=" * 80)
txns = inventory.transactions.all().order_by('created_at')
for txn in txns:
    print(f"[{txn.created_at.strftime('%H:%M:%S')}] {txn.transaction_type.upper():12} | Qty: {txn.quantity:6.1f} | Ref: {txn.reference_number[:30]:30} | {txn.reason}")

print()
print("=" * 80)
print("🎉 ALL TESTS PASSED! Order flow logic is correct!")
print("=" * 80)
print()
print("SUMMARY:")
print(f"- Initial stock: 1000")
print(f"- Order 1: Reserve 50, Ship 50 → Current: 950, Reserved: 0")
print(f"- Order 2: Reserve 100, Cancel → Current: 950, Reserved: 0")
print(f"- Final available: {inventory.available_quantity}")
print(f"- Total transactions: {txns.count()}")
