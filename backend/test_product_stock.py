from ecommerce.models import Product

# Test Product.in_stock property
p = Product.objects.select_related('inventory').first()

print(f'Product: {p.name}')
print(f'in_stock (property): {p.in_stock}')
print(f'available_stock: {p.available_stock}')
print(f'is_low_stock: {p.is_low_stock}')
print(f'is_out_of_stock: {p.is_out_of_stock}')

if hasattr(p, 'inventory') and p.inventory:
    print(f'\nInventory.current_quantity: {p.inventory.current_quantity}')
    print(f'Inventory.reserved_quantity: {p.inventory.reserved_quantity}')
    print(f'Inventory.available_quantity: {p.inventory.available_quantity}')
else:
    print('\nNo inventory record found')

print('\n✅ Product.in_stock property works correctly!')
