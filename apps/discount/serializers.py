from rest_framework import serializers
from .models import Discount
from apps.restaurant.serializers import RestaurantListSerializer
from apps.product.serializers import ProductListSerializer


class DiscountSerializer(serializers.ModelSerializer):
    restaurant = RestaurantListSerializer(read_only=True)
    products = ProductListSerializer(many=True, read_only=True)
    is_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = Discount
        fields = [
            'id', 'name', 'description', 'discount_type', 'discount_value',
            'start_date', 'end_date', 'is_active', 'restaurant', 'products',
            'minimum_order_amount', 'maximum_discount', 'usage_limit',
            'used_count', 'created_at', 'updated_at', 'is_valid'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'used_count']


class DiscountListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    restaurant = RestaurantListSerializer(read_only=True)
    is_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = Discount
        fields = [
            'id', 'name', 'description', 'discount_type', 'discount_value',
            'start_date', 'end_date', 'is_active', 'restaurant',
            'minimum_order_amount', 'maximum_discount', 'is_valid'
        ]


class DiscountCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating discounts"""
    class Meta:
        model = Discount
        fields = [
            'name', 'description', 'discount_type', 'discount_value',
            'start_date', 'end_date', 'is_active', 'restaurant',
            'minimum_order_amount', 'maximum_discount', 'usage_limit'
        ]
