from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Inventory


@receiver(post_save, sender=Product)
def create_inventory_for_product(sender, instance, created, **kwargs):
    """Automatically create inventory record when a new product is created"""
    if created:
        Inventory.objects.get_or_create(
            product=instance,
            defaults={
                'current_quantity': instance.in_stock or 0,
                'min_quantity': 0,
                'max_quantity': None,
                'reserved_quantity': 0
            }
        )