from rest_framework import serializers
from .models import DeliveryZone


class DeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZone
        fields = [
            'id', 'name', 'description', 'delivery_fee',
            'estimated_time', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DeliveryZoneListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    class Meta:
        model = DeliveryZone
        fields = ['id', 'name', 'delivery_fee', 'estimated_time']
