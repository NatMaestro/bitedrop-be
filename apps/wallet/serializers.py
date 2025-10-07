from rest_framework import serializers
from .models import WalletTransaction
from apps.order.serializers import OrderSerializer


class WalletTransactionSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    
    class Meta:
        model = WalletTransaction
        fields = [
            'id', 'type', 'amount', 'points', 'description',
            'order', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class WalletTransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating wallet transactions"""
    class Meta:
        model = WalletTransaction
        fields = ['type', 'amount', 'points', 'description', 'order']


class WalletBalanceSerializer(serializers.Serializer):
    """Serializer for wallet balance information"""
    wallet_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    loyalty_points = serializers.IntegerField()
    total_transactions = serializers.IntegerField()
    recent_transactions = WalletTransactionSerializer(many=True)
