from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import WalletTransaction
from .serializers import WalletTransactionSerializer, WalletTransactionCreateSerializer, WalletBalanceSerializer


class WalletTransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing wallet transactions.
    """
    queryset = WalletTransaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return wallet transactions for the authenticated user"""
        if self.request.user.is_authenticated:
            return WalletTransaction.objects.filter(user=self.request.user)
        else:
            return WalletTransaction.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return WalletTransactionCreateSerializer
        return WalletTransactionSerializer

    def perform_create(self, serializer):
        """Set the user to the current user when creating a transaction"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def balance(self, request):
        """Get wallet balance and recent transactions"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
            
        user = request.user
        recent_transactions = WalletTransaction.objects.filter(
            user=user
        )[:10]  # Last 10 transactions
        
        data = {
            'wallet_balance': user.wallet_balance,
            'loyalty_points': user.loyalty_points,
            'total_transactions': WalletTransaction.objects.filter(user=user).count(),
            'recent_transactions': WalletTransactionSerializer(recent_transactions, many=True).data
        }
        
        serializer = WalletBalanceSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def earned(self, request):
        """Get all earned transactions"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
            
        transactions = WalletTransaction.objects.filter(
            user=request.user,
            type='earned'
        )
        serializer = WalletTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def redeemed(self, request):
        """Get all redeemed transactions"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
            
        transactions = WalletTransaction.objects.filter(
            user=request.user,
            type='redeemed'
        )
        serializer = WalletTransactionSerializer(transactions, many=True)
        return Response(serializer.data)