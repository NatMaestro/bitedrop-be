from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'restaurant', 'rating', 'created_at']
    list_filter = ['rating', 'product__restaurant', 'created_at']
    search_fields = ['user__name', 'user__email', 'product__name', 'restaurant__name', 'comment']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'rating', 'comment')
        }),
        ('Reviewed Items', {
            'fields': ('product', 'restaurant')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )