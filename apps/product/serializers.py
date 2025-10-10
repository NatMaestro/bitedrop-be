from rest_framework import serializers
from .models import Product
from apps.restaurant.serializers import RestaurantListSerializer
from apps.category.serializers import CategoryListSerializer


class ProductSerializer(serializers.ModelSerializer):
    restaurant = RestaurantListSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    is_discounted = serializers.ReadOnlyField()
    final_price = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'discount_price',
            'discount_percentage', 'image', 'category', 'restaurant',
            'in_stock', 'is_flash_sale', 'rating', 'reviews_count',
            'ingredients', 'allergens', 'calories', 'preparation_time',
            'created_at', 'updated_at', 'is_discounted', 'final_price',
            'average_rating', 'total_reviews'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'rating', 'reviews_count']


class ProductListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    restaurant = RestaurantListSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)  # Return category UUID
    is_discounted = serializers.ReadOnlyField()
    final_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'discount_price',
            'discount_percentage', 'image', 'category', 'restaurant', 'in_stock',
            'is_flash_sale', 'rating', 'reviews_count', 'is_discounted',
            'final_price'
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating products"""
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'discount_price',
            'discount_percentage', 'image', 'category', 'restaurant',
            'in_stock', 'is_flash_sale', 'ingredients', 'allergens',
            'calories', 'preparation_time'
        ]
