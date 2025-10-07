from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['id', 'user__name', 'user__email', 'delivery_address']
    list_editable = ['status', 'payment_status']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'total', 'status')
        }),
        ('Delivery', {
            'fields': ('delivery_address', 'delivery_fee', 'delivery_time', 'notes')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__status', 'product__restaurant']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['total_price']