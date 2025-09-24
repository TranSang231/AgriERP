from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "email", "phone", "tax_code")
