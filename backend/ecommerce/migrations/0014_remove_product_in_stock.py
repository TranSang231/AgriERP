# Generated migration to remove Product.in_stock field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_migrate_stock_to_inventory'),
    ]

    operations = [
        # Remove Product.in_stock field from database
        # Stock is now managed exclusively via Inventory.current_quantity
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
    ]
