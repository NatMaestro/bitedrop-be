from django.contrib import admin
from .models import PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'processing_fee', 'is_active', 'created_at']
    list_filter = ['type', 'is_active', 'created_at']
    search_fields = ['name', 'supported_networks']
    list_editable = ['is_active', 'processing_fee']
    ordering = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']