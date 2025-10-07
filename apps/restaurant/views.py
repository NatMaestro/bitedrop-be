from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Restaurant
from .serializers import RestaurantSerializer, RestaurantListSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing restaurants.
    """
    queryset = Restaurant.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_partner']
    search_fields = ['name', 'description', 'cuisine_type']
    ordering_fields = ['name', 'rating', 'created_at']
    ordering = ['-rating', 'name']

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantListSerializer
        return RestaurantSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products for a specific restaurant"""
        restaurant = self.get_object()
        from apps.product.models import Product
        from apps.product.serializers import ProductListSerializer
        
        products = Product.objects.filter(restaurant=restaurant, in_stock=True)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific restaurant"""
        restaurant = self.get_object()
        from apps.review.models import Review
        from apps.review.serializers import ReviewSerializer
        
        reviews = Review.objects.filter(restaurant=restaurant)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)