from django.db import models
from django.core.management import call_command
from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce'

    def ready(self):
        # Auto-create inventory records when app is ready
        import ecommerce.signals
        try:
            # Only run if we're in a proper Django environment
            from django.conf import settings
            if not settings.configured:
                return
                
            # Check if inventory table exists
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='ecommerce_inventory'
                """)
                table_exists = cursor.fetchone() is not None
                
            if table_exists:
                # Check if we have products but no inventory records
                from .models import Product, Inventory
                if Product.objects.exists() and not Inventory.objects.exists():
                    call_command('create_inventory_records')
        except Exception as e:
            # Silently fail in case of any issues
            pass