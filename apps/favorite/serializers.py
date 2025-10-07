from rest_framework import serializers
from .models import Favorite
from apps.restaurant.serializers import RestaurantListSerializer
from apps.product.serializers import ProductListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    restaurant = RestaurantListSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = [
            'id', 'type', 'restaurant', 'product', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class FavoriteCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating favorites"""
    class Meta:
        model = Favorite
        fields = ['type', 'restaurant', 'product']

    def validate(self, attrs):
        """Validate that exactly one of restaurant or product is set based on type"""
        type = attrs.get('type')
        restaurant = attrs.get('restaurant')
        product = attrs.get('product')
        
        if type == 'restaurant' and not restaurant:
            raise serializers.ValidationError("Restaurant must be set when type is 'restaurant'")
        elif type == 'product' and not product:
            raise serializers.ValidationError("Product must be set when type is 'product'")
        
        if type == 'restaurant' and product:
            raise serializers.ValidationError("Product should not be set when type is 'restaurant'")
        elif type == 'product' and restaurant:
            raise serializers.ValidationError("Restaurant should not be set when type is 'product'")
        
        return attrs
