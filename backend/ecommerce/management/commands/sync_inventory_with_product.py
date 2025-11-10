"""
Management command to sync Inventory.current_quantity with Product.in_stock
This fixes any discrepancies between the two fields
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from ecommerce.models import Product, Inventory


class Command(BaseCommand):
    help = 'Sync Inventory.current_quantity with Product.in_stock to fix discrepancies'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Actually fix the discrepancies (dry-run by default)',
        )

    def handle(self, *args, **options):
        fix_mode = options['fix']
        
        if not fix_mode:
            self.stdout.write(self.style.WARNING('Running in DRY-RUN mode. Use --fix to apply changes.'))
        
        # Get all products with inventory
        products_with_inventory = Product.objects.filter(inventory__isnull=False).select_related('inventory')
        
        discrepancies = []
        total_checked = 0
        
        for product in products_with_inventory:
            total_checked += 1
            inventory = product.inventory
            
            product_stock = product.in_stock or 0.0
            inventory_stock = inventory.current_quantity or 0.0
            
            if product_stock != inventory_stock:
                diff = product_stock - inventory_stock
                discrepancies.append({
                    'product_id': product.id,
                    'product_name': str(product.name) if product.name else 'N/A',
                    'product_in_stock': product_stock,
                    'inventory_current_quantity': inventory_stock,
                    'difference': diff
                })
                
                if fix_mode:
                    # Sync Inventory to match Product
                    inventory.current_quantity = product_stock
                    inventory.save(update_fields=['current_quantity', 'updated_at'])
        
        # Display results
        self.stdout.write(f'\nTotal products checked: {total_checked}')
        self.stdout.write(f'Discrepancies found: {len(discrepancies)}\n')
        
        if discrepancies:
            self.stdout.write(self.style.ERROR('Found discrepancies:'))
            for item in discrepancies:
                self.stdout.write(
                    f"  Product {item['product_id']} ({item['product_name']}):\n"
                    f"    Product.in_stock: {item['product_in_stock']}\n"
                    f"    Inventory.current_quantity: {item['inventory_current_quantity']}\n"
                    f"    Difference: {item['difference']}\n"
                )
            
            if fix_mode:
                self.stdout.write(self.style.SUCCESS(f'\n✓ Fixed {len(discrepancies)} discrepancies!'))
            else:
                self.stdout.write(self.style.WARNING(f'\n⚠ Run with --fix to fix these discrepancies'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ All inventory records are in sync with products!'))
