from django.contrib import admin
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_partner', 'rating', 'is_active', 'created_at']
    list_filter = ['is_partner', 'is_active', 'created_at', 'rating']
    search_fields = ['name', 'description', 'address', 'email']
    list_editable = ['is_partner', 'is_active']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'logo', 'banner')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Settings', {
            'fields': ('is_partner', 'is_active', 'rating', 'delivery_time')
        }),
        ('Pricing', {
            'fields': ('delivery_fee', 'minimum_order')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )