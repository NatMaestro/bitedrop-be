from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Notification
from .serializers import NotificationSerializer, NotificationCreateSerializer, NotificationUpdateSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing notifications.
    """
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'is_read']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return notifications for the authenticated user"""
        if self.request.user.is_authenticated:
            return Notification.objects.filter(user=self.request.user)
        else:
            return Notification.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return NotificationUpdateSerializer
        return NotificationSerializer

    def perform_create(self, serializer):
        """Set the user to the current user when creating a notification"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get all unread notifications"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
            
        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
            
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a specific notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'message': 'Notification marked as read'})