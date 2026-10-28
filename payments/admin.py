from django.contrib import admin
from .models import Package, Payment

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price_rial", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("public_id", "user", "package", "amount_rial", "status", "created_at")
    list_filter = ("status", "provider", "created_at")
    search_fields = ("public_id", "user__username", "provider_reference")
    readonly_fields = ("public_id", "created_at", "paid_at")