from ecommerce.models import InventoryTransaction, Inventory, Product
from django.db.models import Count

print("=" * 80)
print("INVENTORY TRANSACTION HISTORY CHECK")
print("=" * 80)

# Total statistics
total_txns = InventoryTransaction.objects.count()
total_inv = Inventory.objects.count()

print(f"\n📊 Total Transactions: {total_txns}")
print(f"📦 Total Inventories: {total_inv}")

# By type
print("\n📈 Transactions by Type:")
for tx_type, label in InventoryTransaction.TRANSACTION_TYPES:
    count = InventoryTransaction.objects.filter(transaction_type=tx_type).count()
    if count > 0:
        print(f"  {label:15} ({tx_type:10}): {count:5}")

# Recent transactions
print("\n🕒 Recent 15 Transactions:")
print("-" * 80)
print(f"{'Date':<18} {'Type':<10} {'Qty':<10} {'Reference':<30}")
print("-" * 80)

txns = InventoryTransaction.objects.select_related(
    'inventory__product__name'
).order_by('-created_at')[:15]

for txn in txns:
    date_str = txn.created_at.strftime('%Y-%m-%d %H:%M')
    ref = txn.reference_number[:28] if txn.reference_number else ""
    print(f"{date_str:<18} {txn.transaction_type:<10} {txn.quantity:<10.2f} {ref:<30}")

# Goods Receipt transactions
print("\n📦 Goods Receipt Transactions:")
print("-" * 80)
gr_txns = InventoryTransaction.objects.filter(
    reference_number__startswith='GR-'
).order_by('-created_at')[:10]

if gr_txns.exists():
    print(f"{'Date':<18} {'Type':<10} {'Qty':<10} {'Reference':<25}")
    print("-" * 80)
    for txn in gr_txns:
        date_str = txn.created_at.strftime('%Y-%m-%d %H:%M')
        print(f"{date_str:<18} {txn.transaction_type:<10} {txn.quantity:<10.2f} {txn.reference_number:<25}")
else:
    print("⚠️  No GR transactions found")

# Apply/Unapply pairs
print("\n🔄 Apply/Unapply Pairs:")
print("-" * 80)
unapply_txns = InventoryTransaction.objects.filter(
    reference_number__contains='UNAPPLY'
).order_by('-created_at')[:5]

if unapply_txns.exists():
    for txn in unapply_txns:
        print(f"\n🔸 {txn.reference_number}")
        print(f"   Type: {txn.transaction_type}, Qty: {txn.quantity}, Date: {txn.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        # Find matching apply
        gr_id = txn.reference_number.replace('GR-UNAPPLY-', '').replace('UNAPPLY-', '')
        apply = InventoryTransaction.objects.filter(
            reference_number=f'GR-{gr_id}',
            inventory=txn.inventory
        ).first()
        
        if apply:
            print(f"   ✅ Matching APPLY: {apply.reference_number} (Qty: {apply.quantity})")
        else:
            print(f"   ⚠️  No matching APPLY found")
else:
    print("ℹ️  No UNAPPLY transactions yet")

# Sample product history
print("\n📝 Sample Product Transaction History:")
print("-" * 80)
inv = Inventory.objects.annotate(txn_count=Count('transactions')).filter(txn_count__gt=0).first()

if inv:
    try:
        product_name = inv.product.name.origin[:40]
    except:
        product_name = "Unknown"
    
    print(f"\nProduct: {product_name}")
    print(f"Current Stock: {inv.current_quantity}")
    print(f"Transactions: {inv.transactions.count()}")
    
    print(f"\n{'Date':<18} {'Type':<10} {'Qty':<10} {'Running':<10} {'Reference':<20}")
    print("-" * 80)
    
    running = 0.0
    for txn in inv.transactions.order_by('created_at'):
        running += txn.quantity
        date_str = txn.created_at.strftime('%Y-%m-%d %H:%M')
        ref = (txn.reference_number[:18] + "...") if len(txn.reference_number) > 20 else txn.reference_number
        print(f"{date_str:<18} {txn.transaction_type:<10} {txn.quantity:<10.2f} {running:<10.2f} {ref:<20}")
    
    print(f"\n✅ Calculated: {running:.2f}, Actual: {inv.current_quantity:.2f}")
    if abs(running - inv.current_quantity) < 0.01:
        print("✅ Stock matches transaction history!")
    else:
        print(f"❌ WARNING: Mismatch of {abs(running - inv.current_quantity):.2f}")

print("\n" + "=" * 80)
print("✅ CHECK COMPLETE")
print("=" * 80)
