from django.db import models
from django.utils import timezone
import uuid


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'user_account.User',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews'
    )
    restaurant = models.ForeignKey(
        'restaurant.Restaurant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [
            ['user', 'product'],
            ['user', 'restaurant']
        ]

    def __str__(self):
        if self.product:
            return f"{self.user.name} - {self.product.name} - {self.rating} stars"
        elif self.restaurant:
            return f"{self.user.name} - {self.restaurant.name} - {self.rating} stars"
        return f"{self.user.name} - {self.rating} stars"

    def clean(self):
        """Validate that exactly one of product or restaurant is set"""
        from django.core.exceptions import ValidationError
        
        if not self.product and not self.restaurant:
            raise ValidationError("Either product or restaurant must be set")
        
        if self.product and self.restaurant:
            raise ValidationError("Only one of product or restaurant should be set")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
        # Update product/restaurant rating and review count
        if self.product:
            self._update_product_stats()
        elif self.restaurant:
            self._update_restaurant_stats()

    def _update_product_stats(self):
        """Update product rating and review count"""
        reviews = Review.objects.filter(product=self.product)
        if reviews.exists():
            avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.product.rating = round(avg_rating, 2)
            self.product.reviews_count = reviews.count()
            self.product.save(update_fields=['rating', 'reviews_count'])

    def _update_restaurant_stats(self):
        """Update restaurant rating"""
        reviews = Review.objects.filter(restaurant=self.restaurant)
        if reviews.exists():
            avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.restaurant.rating = round(avg_rating, 2)
            self.restaurant.save(update_fields=['rating'])