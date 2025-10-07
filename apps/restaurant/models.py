from django.db import models
from django.utils import timezone
import uuid


class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo = models.URLField(blank=True, null=True)
    banner = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    delivery_time = models.CharField(max_length=50, blank=True, null=True)
    cuisine_type = models.JSONField(default=list, blank=True)  # List of cuisine types
    is_partner = models.BooleanField(default=False)
    active_discounts = models.IntegerField(default=0)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_hours = models.JSONField(default=dict, blank=True)  # Opening hours for each day
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        from review.models import Review
        reviews = Review.objects.filter(restaurant=self)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0.00
        return 0.00

    @property
    def total_reviews(self):
        """Get total number of reviews"""
        from review.models import Review
        return Review.objects.filter(restaurant=self).count()