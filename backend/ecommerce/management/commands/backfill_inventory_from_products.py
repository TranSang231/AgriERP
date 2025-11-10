from django.core.management.base import BaseCommand
from django.db import transaction
from ecommerce.models import Product, Inventory


class Command(BaseCommand):
    help = 'Backfill inventory records from existing products with in_stock values'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually making changes',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        self.stdout.write('Backfilling inventory records from products...')
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        products = Product.objects.all()
        total_products = products.count()
        
        self.stdout.write(f'Found {total_products} products to process')
        
        with transaction.atomic():
            for product in products:
                in_stock = product.in_stock or 0
                
                try:
                    inventory, created = Inventory.objects.get_or_create(
                        product=product,
                        defaults={
                            'current_quantity': in_stock,
                            'min_quantity': 0,
                            'max_quantity': None,
                            'reserved_quantity': 0
                        }
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✓ Created inventory for product #{product.id}: '
                                f'{product.name} (stock: {in_stock})'
                            )
                        )
                    else:
                        # Update existing inventory if current_quantity differs from in_stock
                        if inventory.current_quantity != in_stock:
                            if not dry_run:
                                inventory.current_quantity = in_stock
                                inventory.save(update_fields=['current_quantity', 'updated_at'])
                            updated_count += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f'  ⟳ Updated inventory for product #{product.id}: '
                                    f'{product.name} ({inventory.current_quantity} → {in_stock})'
                                )
                            )
                        else:
                            skipped_count += 1
                            if options.get('verbosity', 1) >= 2:
                                self.stdout.write(
                                    f'  - Skipped product #{product.id}: {product.name} (already synced)'
                                )
                
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'  ✗ Error processing product #{product.id}: {str(e)}'
                        )
                    )
            
            if dry_run:
                self.stdout.write(self.style.WARNING('\nDRY RUN - Rolling back transaction'))
                transaction.set_rollback(True)
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(
            self.style.SUCCESS(
                f'Backfill {"would be" if dry_run else ""} complete!\n'
                f'  Total products: {total_products}\n'
                f'  Created: {created_count}\n'
                f'  Updated: {updated_count}\n'
                f'  Skipped (already synced): {skipped_count}'
            )
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    '\nRun without --dry-run to apply these changes'
                )
            )
