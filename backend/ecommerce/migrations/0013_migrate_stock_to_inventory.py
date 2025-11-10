# Generated migration to move Product.in_stock to Inventory.current_quantity

from django.db import migrations


def migrate_stock_to_inventory(apps, schema_editor):
    """
    Migrate all Product.in_stock values to Inventory.current_quantity
    This ensures Inventory becomes the single source of truth
    """
    Product = apps.get_model('ecommerce', 'Product')
    Inventory = apps.get_model('ecommerce', 'Inventory')
    
    migrated_count = 0
    created_count = 0
    
    for product in Product.objects.all():
        in_stock_value = product.in_stock if product.in_stock is not None else 0.0
        
        # Get or create inventory for this product
        inventory, created = Inventory.objects.get_or_create(
            product=product,
            defaults={
                'current_quantity': in_stock_value,
                'min_quantity': 0.0,
                'max_quantity': None,
                'reserved_quantity': 0.0,
            }
        )
        
        if created:
            created_count += 1
            print(f"Created Inventory for Product {product.id}: stock={in_stock_value}")
        else:
            # Update existing inventory with product stock value
            inventory.current_quantity = in_stock_value
            inventory.save(update_fields=['current_quantity'])
            migrated_count += 1
            print(f"Updated Inventory for Product {product.id}: stock={in_stock_value}")
    
    print(f"\nMigration complete:")
    print(f"  - Created {created_count} new Inventory records")
    print(f"  - Updated {migrated_count} existing Inventory records")


def reverse_migrate(apps, schema_editor):
    """
    Reverse migration: copy Inventory.current_quantity back to Product.in_stock
    This allows rolling back if needed
    """
    Product = apps.get_model('ecommerce', 'Product')
    Inventory = apps.get_model('ecommerce', 'Inventory')
    
    for product in Product.objects.all():
        try:
            inventory = Inventory.objects.get(product=product)
            product.in_stock = inventory.current_quantity
            product.save(update_fields=['in_stock'])
            print(f"Restored Product {product.id} stock from Inventory: {inventory.current_quantity}")
        except Inventory.DoesNotExist:
            product.in_stock = 0.0
            product.save(update_fields=['in_stock'])
            print(f"Product {product.id} has no Inventory, set stock to 0")


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0012_alter_goodsreceipt_note_and_more'),
    ]

    operations = [
        # Migrate data from Product.in_stock to Inventory.current_quantity
        migrations.RunPython(
            migrate_stock_to_inventory,
            reverse_code=reverse_migrate
        ),
    ]
