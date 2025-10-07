from django.db import models
from django.utils import timezone
import uuid


class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # Relationships - can be global, restaurant-specific, or product-specific
    restaurant = models.ForeignKey(
        'restaurant.Restaurant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='discounts'
    )
    products = models.ManyToManyField(
        'product.Product',
        blank=True,
        related_name='discounts'
    )
    
    # Usage limits
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    usage_limit = models.PositiveIntegerField(blank=True, null=True)  # Total usage limit
    used_count = models.PositiveIntegerField(default=0)  # Current usage count
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.discount_value}%"

    @property
    def is_valid(self):
        """Check if discount is currently valid"""
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            (self.usage_limit is None or self.used_count < self.usage_limit)
        )

    def can_be_used(self, order_amount):
        """Check if discount can be used for a given order amount"""
        return (
            self.is_valid and
            order_amount >= self.minimum_order_amount
        )

    def calculate_discount(self, order_amount):
        """Calculate discount amount for given order amount"""
        if not self.can_be_used(order_amount):
            return 0.00
        
        if self.discount_type == 'percentage':
            discount_amount = (order_amount * self.discount_value) / 100
        else:  # fixed
            discount_amount = self.discount_value
        
        # Apply maximum discount limit if set
        if self.maximum_discount:
            discount_amount = min(discount_amount, self.maximum_discount)
        
        return discount_amount