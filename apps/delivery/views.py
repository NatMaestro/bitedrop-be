from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import DeliveryZone
from .serializers import DeliveryZoneSerializer, DeliveryZoneListSerializer


class DeliveryZoneViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing delivery zones.
    """
    queryset = DeliveryZone.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'delivery_fee']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return DeliveryZoneListSerializer
        return DeliveryZoneSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]