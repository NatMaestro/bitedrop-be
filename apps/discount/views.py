from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Discount
from .serializers import DiscountSerializer, DiscountListSerializer, DiscountCreateUpdateSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing discounts.
    Multi-tenant: Restaurant admins and staff only see their restaurant's discounts + global discounts.
    """
    queryset = Discount.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['discount_type', 'restaurant', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'discount_value']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Filter discounts based on user role for multi-tenant support.
        - Super admin: sees all discounts
        - Restaurant admin: sees their restaurant's discounts + global discounts
        - Staff: sees their restaurant's discounts + global discounts
        - Regular users/unauthorized: sees all active discounts
        """
        queryset = Discount.objects.all()
        user = self.request.user
        
        if user.is_authenticated:
            # Super admin sees all discounts
            if user.role == 'admin' or user.is_superuser:
                return queryset
            
            # Restaurant admin sees their discounts + global discounts
            elif user.role == 'restaurant_admin' and user.restaurant:
                return queryset.filter(
                    models.Q(restaurant=user.restaurant) |
                    models.Q(restaurant__isnull=True)
                )
            
            # Staff sees their restaurant's discounts + global discounts
            elif user.role == 'staff' and user.restaurant:
                return queryset.filter(
                    models.Q(restaurant=user.restaurant) |
                    models.Q(restaurant__isnull=True)
                )
        
        # Regular users and unauthorized users see all active discounts
        return queryset

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

    def perform_create(self, serializer):
        """
        Enforce restaurant assignment for restaurant admins and staff.
        Restaurant admins can only create discounts for their restaurant.
        """
        user = self.request.user
        
        if user.role == 'restaurant_admin' and user.restaurant:
            # Force restaurant admin to create discounts for their restaurant only
            serializer.save(restaurant=user.restaurant)
        elif user.role == 'staff' and user.restaurant:
            # Staff can also create discounts for their restaurant
            serializer.save(restaurant=user.restaurant)
        else:
            # Admin or regular users can specify restaurant (or leave null for global)
            serializer.save()

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active discounts (filtered by restaurant for multi-tenant)"""
        from django.utils import timezone
        now = timezone.now()
        discounts = self.get_queryset().filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        )
        serializer = DiscountListSerializer(discounts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def global_discounts(self, request):
        """Get all global discounts (not restaurant-specific)"""
        discounts = self.get_queryset().filter(
            is_active=True,
            restaurant__isnull=True
        )
        serializer = DiscountListSerializer(discounts, many=True)
        return Response(serializer.data)