from django.core.management.base import BaseCommand
from django.db import transaction
from ecommerce.models import InventoryConfiguration


class Command(BaseCommand):
    help = 'Initialize default inventory configuration if none exists'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset to default configuration (deactivates all existing configs)',
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            if options['reset']:
                # Deactivate all existing configurations
                InventoryConfiguration.objects.all().update(is_active=False)
                self.stdout.write(self.style.WARNING('All existing configurations deactivated'))

            # Get or create active configuration
            config = InventoryConfiguration.get_active_config()
            
            if config.created_at == config.updated_at and not options['reset']:
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Created new inventory configuration with default settings (ID: {config.id})'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Active inventory configuration already exists (ID: {config.id})'
                ))

            # Display current configuration
            self.stdout.write(self.style.SUCCESS('\nCurrent Configuration:'))
            self.stdout.write(f'  Low Stock Threshold Type: {config.low_stock_threshold_type}')
            self.stdout.write(f'  Low Stock Threshold Value: {config.low_stock_threshold_value}')
            self.stdout.write(f'  Out of Stock Threshold: {config.out_of_stock_threshold}')
            self.stdout.write(f'  Enable Auto Reorder: {config.enable_auto_reorder}')
            self.stdout.write(f'  Allow Negative Stock: {config.allow_negative_stock}')
            self.stdout.write(f'  Stock Labels: "{config.in_stock_label}" / "{config.low_stock_label}" / "{config.out_of_stock_label}"')
            
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Inventory configuration is ready!'
            ))
