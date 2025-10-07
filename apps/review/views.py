from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reviews.
    """
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'restaurant', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return reviews, filtered by user if not staff"""
        if self.request.user.is_staff:
            return Review.objects.all()
        elif self.request.user.is_authenticated:
            return Review.objects.filter(user=self.request.user)
        else:
            return Review.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        """Set the user to the current user when creating a review"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get all reviews by the authenticated user"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
            
        reviews = Review.objects.filter(user=request.user)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def high_rated(self, request):
        """Get all high-rated reviews (4+ stars)"""
        reviews = Review.objects.filter(rating__gte=4)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)