from rest_framework import serializers
from .models import Notification
from apps.order.serializers import OrderSerializer
from apps.discount.serializers import DiscountListSerializer


class NotificationSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    discount = DiscountListSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'type', 'is_read',
            'order', 'discount', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications"""
    class Meta:
        model = Notification
        fields = [
            'title', 'message', 'type', 'order', 'discount'
        ]


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating notification read status"""
    class Meta:
        model = Notification
        fields = ['is_read']
