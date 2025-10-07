from rest_framework import serializers
from .models import Order, OrderItem
from apps.product.serializers import ProductListSerializer
from apps.user_account.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'quantity', 'unit_price', 'total_price'
        ]
        read_only_fields = ['id', 'total_price']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating order items"""
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.ReadOnlyField()
    restaurants = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total', 'status', 'delivery_address',
            'delivery_fee', 'payment_method', 'payment_status',
            'delivery_time', 'notes', 'created_at', 'updated_at',
            'items', 'items_count', 'restaurants'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_restaurants(self, obj):
        """Get restaurants involved in this order"""
        from apps.restaurant.serializers import RestaurantListSerializer
        restaurants = obj.restaurants
        return RestaurantListSerializer(restaurants, many=True).data


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders"""
    items = OrderItemCreateSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'delivery_address', 'delivery_fee', 'payment_method',
            'notes', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        total = 0
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            total += item_data['unit_price'] * item_data['quantity']
        
        order.total = total
        order.save()
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating order status"""
    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'delivery_time']
