from rest_framework import serializers
from .models import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'name', 'type', 'is_active', 'supported_networks',
            'processing_fee', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentMethodListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'type', 'processing_fee']
