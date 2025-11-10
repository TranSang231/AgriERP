from django.core.management.base import BaseCommand
from django.db import transaction
from ecommerce.models import Product, Inventory


class Command(BaseCommand):
    help = 'Create inventory records for existing products'

    def handle(self, *args, **options):
        self.stdout.write('Creating inventory records for existing products...')
        
        created_count = 0
        updated_count = 0
        
        with transaction.atomic():
            products = Product.objects.all()
            
            for product in products:
                inventory, created = Inventory.objects.get_or_create(
                    product=product,
                    defaults={
                        'current_quantity': product.in_stock or 0,
                        'min_quantity': 0,
                        'max_quantity': None,
                        'reserved_quantity': 0
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'Created inventory for product: {product}')
                else:
                    # Update existing inventory with product's in_stock value
                    if inventory.current_quantity != product.in_stock:
                        inventory.current_quantity = product.in_stock or 0
                        inventory.save()
                        updated_count += 1
                        self.stdout.write(f'Updated inventory for product: {product}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(products)} products. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )
