from ecommerce.models import Inventory, InventoryTransaction
from django.db.models import Count, Sum

print("=" * 80)
print("CHECKING STOCK VS TRANSACTION MISMATCH")
print("=" * 80)

# Get all inventories with transactions
inventories = Inventory.objects.annotate(
    txn_count=Count('transactions')
).filter(txn_count__gt=0)

print(f"\nFound {inventories.count()} inventories with transactions\n")

mismatches = []

for inv in inventories:
    # Calculate from transactions
    txn_sum = inv.transactions.aggregate(total=Sum('quantity'))['total'] or 0.0
    actual_stock = inv.current_quantity or 0.0
    
    diff = abs(txn_sum - actual_stock)
    
    if diff > 0.01:  # More than 1 cent difference
        try:
            product_name = inv.product.name.origin[:30]
        except:
            product_name = "Unknown"
        
        mismatches.append({
            'product': product_name,
            'calculated': txn_sum,
            'actual': actual_stock,
            'diff': diff,
            'txn_count': inv.transactions.count()
        })

if mismatches:
    print(f"❌ Found {len(mismatches)} products with stock mismatch:\n")
    print(f"{'Product':<32} {'Calculated':<12} {'Actual':<12} {'Diff':<12} {'Txns':<6}")
    print("-" * 80)
    
    for m in mismatches:
        print(f"{m['product']:<32} {m['calculated']:<12.2f} {m['actual']:<12.2f} {m['diff']:<12.2f} {m['txn_count']:<6}")
    
    print("\n⚠️  POSSIBLE CAUSES:")
    print("1. Stock was changed directly (without transaction log)")
    print("2. Old data from before transaction logging was implemented")
    print("3. Manual database updates")
    print("4. Migration didn't sync properly")
    
    print("\n💡 RECOMMENDED FIX:")
    print("Run: python manage.py sync_inventory_with_product")
    print("Or create adjustment transactions to match current stock")
    
else:
    print("✅ All inventories match their transaction history perfectly!")

print("\n" + "=" * 80)
