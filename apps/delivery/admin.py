from django.contrib import admin
from .models import DeliveryZone


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'delivery_fee', 'estimated_time', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'delivery_fee']
    ordering = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']