from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Favorite
from .serializers import FavoriteSerializer, FavoriteCreateSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing favorites.
    """
    queryset = Favorite.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'restaurant', 'product']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return favorites for the authenticated user"""
        if self.request.user.is_authenticated:
            return Favorite.objects.filter(user=self.request.user)
        else:
            return Favorite.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return FavoriteCreateSerializer
        return FavoriteSerializer

    def perform_create(self, serializer):
        """Set the user to the current user when creating a favorite"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def restaurants(self, request):
        """Get all favorite restaurants for the user"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
            
        favorites = Favorite.objects.filter(
            user=request.user,
            type='restaurant'
        )
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def products(self, request):
        """Get all favorite products for the user"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
            
        favorites = Favorite.objects.filter(
            user=request.user,
            type='product'
        )
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)