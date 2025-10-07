from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'category', 'price', 'is_flash_sale', 'in_stock', 'created_at']
    list_filter = ['category', 'restaurant', 'is_flash_sale', 'in_stock', 'created_at']
    search_fields = ['name', 'description', 'ingredients']
    list_editable = ['is_flash_sale', 'in_stock']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'rating', 'reviews_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image', 'category', 'restaurant')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price', 'discount_percentage')
        }),
        ('Settings', {
            'fields': ('in_stock', 'is_flash_sale', 'rating', 'reviews_count')
        }),
        ('Details', {
            'fields': ('ingredients', 'allergens', 'calories', 'preparation_time')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )