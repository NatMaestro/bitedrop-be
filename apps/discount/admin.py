from django.contrib import admin
from .models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_type', 'discount_value', 'is_active', 'start_date', 'end_date', 'used_count']
    list_filter = ['discount_type', 'is_active', 'restaurant', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'used_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'discount_type', 'discount_value')
        }),
        ('Validity', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Scope', {
            'fields': ('restaurant', 'products')
        }),
        ('Limits', {
            'fields': ('minimum_order_amount', 'maximum_discount', 'usage_limit', 'used_count')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )