from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Discount
from .serializers import DiscountSerializer, DiscountListSerializer, DiscountCreateUpdateSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing discounts.
    """
    queryset = Discount.objects.all()  # Show all discounts for admin management
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['discount_type', 'restaurant', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'discount_value']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return DiscountListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DiscountCreateUpdateSerializer
        return DiscountSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active discounts"""
        from django.utils import timezone
        now = timezone.now()
        discounts = Discount.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        )
        serializer = DiscountListSerializer(discounts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def global_discounts(self, request):
        """Get all global discounts (not restaurant-specific)"""
        discounts = Discount.objects.filter(
            is_active=True,
            restaurant__isnull=True
        )
        serializer = DiscountListSerializer(discounts, many=True)
        return Response(serializer.data)