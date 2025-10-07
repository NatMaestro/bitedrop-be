from rest_framework import serializers
from .models import Review
from apps.restaurant.serializers import RestaurantListSerializer
from apps.product.serializers import ProductListSerializer
from apps.user_account.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    restaurant = RestaurantListSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'product', 'restaurant', 'rating',
            'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reviews"""
    class Meta:
        model = Review
        fields = ['product', 'restaurant', 'rating', 'comment']

    def validate(self, attrs):
        """Validate that exactly one of product or restaurant is set"""
        product = attrs.get('product')
        restaurant = attrs.get('restaurant')
        
        if not product and not restaurant:
            raise serializers.ValidationError("Either product or restaurant must be set")
        
        if product and restaurant:
            raise serializers.ValidationError("Only one of product or restaurant should be set")
        
        return attrs


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
