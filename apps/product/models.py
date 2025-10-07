from django.db import models
from django.utils import timezone
import uuid


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percentage = models.IntegerField(default=0)
    image = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        'category.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    restaurant = models.ForeignKey(
        'restaurant.Restaurant',
        on_delete=models.CASCADE,
        related_name='products'
    )
    in_stock = models.BooleanField(default=True)
    is_flash_sale = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    reviews_count = models.IntegerField(default=0)
    ingredients = models.JSONField(default=list, blank=True)  # List of ingredients
    allergens = models.JSONField(default=list, blank=True)  # List of allergens
    calories = models.IntegerField(blank=True, null=True)
    preparation_time = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    @property
    def is_discounted(self):
        """Check if product has discount"""
        return self.discount_price is not None and self.discount_price < self.price

    @property
    def final_price(self):
        """Get the final price (discounted or regular)"""
        return self.discount_price if self.is_discounted else self.price

    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        from review.models import Review
        reviews = Review.objects.filter(product=self)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0.00
        return 0.00

    @property
    def total_reviews(self):
        """Get total number of reviews"""
        from review.models import Review
        return Review.objects.filter(product=self).count()