from django.contrib import admin
from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'restaurant', 'product', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['user__name', 'user__email', 'restaurant__name', 'product__name']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at']