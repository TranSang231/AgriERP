from ecommerce.models import Inventory, InventoryTransaction
from django.db.models import Count

# Find inventory with transactions
inv = Inventory.objects.annotate(
    txn_count=Count('transactions')
).filter(txn_count__gt=0).first()

if not inv:
    print("No inventory with transactions found!")
else:
    print(f"Inventory ID: {inv.id}")
    try:
        print(f"Product: {inv.product.name.origin}")
    except:
        print(f"Product: {inv.product_id}")
    
    print(f"\nTransactions ({inv.transactions.count()}):")
    print("-" * 80)
    print(f"{'ID':<38} {'Type':<10} {'Qty':<10} {'Reference':<30}")
    print("-" * 80)
    
    for txn in inv.transactions.all()[:5]:
        print(f"{str(txn.id):<38} {txn.transaction_type:<10} {txn.quantity:<10.2f} {txn.reference_number:<30}")
    
    # Test serializer
    from ecommerce.serializers import InventoryTransactionSerializer
    from django.db.models import Count
    
    txns = inv.transactions.all()[:2]
    serializer = InventoryTransactionSerializer(txns, many=True)
    
    print(f"\n\nSerializer output ({len(serializer.data)} items):")
    if serializer.data:
        print("Keys:", list(serializer.data[0].keys()) if serializer.data else "No data")
        for item in serializer.data:
            print(f"\n  Transaction:")
            for key, val in item.items():
                print(f"    {key}: {val}")
    else:
        print("  (empty)")
