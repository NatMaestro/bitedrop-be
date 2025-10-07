from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    
    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'logo', 'banner', 'description', 'rating',
            'delivery_time', 'cuisine_type', 'is_partner', 'active_discounts',
            'address', 'phone', 'email', 'opening_hours', 'delivery_fee',
            'minimum_order', 'is_active', 'created_at', 'updated_at',
            'average_rating', 'total_reviews'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'rating']


class RestaurantListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'logo', 'description', 'rating', 'delivery_time',
            'cuisine_type', 'is_partner', 'delivery_fee', 'minimum_order',
            'average_rating'
        ]
