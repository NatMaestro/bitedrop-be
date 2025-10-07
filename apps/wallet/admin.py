from django.contrib import admin
from .models import WalletTransaction


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'amount', 'points', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['user__name', 'user__email', 'description']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at']
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('user', 'type', 'amount', 'points', 'description')
        }),
        ('Related Order', {
            'fields': ('order',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        })
    )