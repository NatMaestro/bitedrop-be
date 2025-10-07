from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders.
    """
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'payment_method']
    ordering_fields = ['created_at', 'total']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return orders for the authenticated user"""
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        """Set the user to the current user when creating an order"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            return Response({'message': 'Order cancelled successfully'})
        return Response(
            {'error': 'Order cannot be cancelled at this stage'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm an order (for restaurant staff)"""
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'confirmed'
            order.save()
            return Response({'message': 'Order confirmed successfully'})
        return Response(
            {'error': 'Order cannot be confirmed at this stage'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def mark_delivered(self, request, pk=None):
        """Mark an order as delivered"""
        order = self.get_object()
        if order.status == 'delivering':
            order.status = 'delivered'
            order.save()
            return Response({'message': 'Order marked as delivered'})
        return Response(
            {'error': 'Order cannot be marked as delivered at this stage'},
            status=status.HTTP_400_BAD_REQUEST
        )