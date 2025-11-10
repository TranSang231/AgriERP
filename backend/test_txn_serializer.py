from ecommerce.models import Inventory
from ecommerce.serializers import InventoryTransactionSerializer

inv = Inventory.objects.filter(transactions__isnull=False).first()
print(f'Inventory ID: {inv.id}')
print(f'Product: {inv.product.name.origin}')
print(f'Transactions: {inv.transactions.count()}')

txns = inv.transactions.all()[:3]
serializer = InventoryTransactionSerializer(txns, many=True)

print('\nSerialized data:')
for txn_data in serializer.data:
    print(f"\n  - ID: {txn_data.get('id')}")
    print(f"    Type: {txn_data.get('transaction_type')}")
    print(f"    Quantity: {txn_data.get('quantity')}")
    print(f"    Reference: {txn_data.get('reference_number')}")
    print(f"    Reason: {txn_data.get('reason')}")
    print(f"    Created: {txn_data.get('created_at')}")
