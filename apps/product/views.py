from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer, ProductCreateUpdateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    Multi-tenant: Restaurant admins and staff only see their restaurant's products.
    """
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['restaurant', 'category', 'is_flash_sale', 'in_stock']
    search_fields = ['name', 'description', 'ingredients']
    ordering_fields = ['name', 'price', 'rating', 'created_at']
    ordering = ['-rating', 'name']

    def get_queryset(self):
        """
        Filter products based on user role for multi-tenant support.
        - Super admin: sees all products
        - Restaurant admin: sees only their restaurant's products
        - Staff: sees only their restaurant's products
        - Regular users/unauthorized: sees all in-stock products
        """
        queryset = Product.objects.all()
        user = self.request.user
        
        if user.is_authenticated:
            # Super admin sees all products
            if user.role == 'admin' or user.is_superuser:
                return queryset
            
            # Restaurant admin sees only their restaurant's products
            elif user.role == 'restaurant_admin' and user.restaurant:
                return queryset.filter(restaurant=user.restaurant)
            
            # Staff sees only their restaurant's products
            elif user.role == 'staff' and user.restaurant:
                return queryset.filter(restaurant=user.restaurant)
            
            # Regular users see all in-stock products
            else:
                return queryset.filter(in_stock=True)
        
        # Unauthorized users see all in-stock products
        return queryset.filter(in_stock=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

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
        Restaurant admins can only create products for their restaurant.
        """
        user = self.request.user
        
        if user.role == 'restaurant_admin' and user.restaurant:
            # Force restaurant admin to create products for their restaurant only
            serializer.save(restaurant=user.restaurant)
        elif user.role == 'staff' and user.restaurant:
            # Staff can also create products for their restaurant
            serializer.save(restaurant=user.restaurant)
        else:
            # Admin or regular users can specify restaurant
            serializer.save()

    @action(detail=False, methods=['get'])
    def flash_sale(self, request):
        """Get all flash sale products (filtered by restaurant for multi-tenant)"""
        products = self.get_queryset().filter(is_flash_sale=True, in_stock=True)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def discounted(self, request):
        """Get all discounted products (filtered by restaurant for multi-tenant)"""
        products = self.get_queryset().filter(
            discount_price__isnull=False,
            in_stock=True
        )
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific product"""
        product = self.get_object()
        from apps.review.models import Review
        from apps.review.serializers import ReviewSerializer
        
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)