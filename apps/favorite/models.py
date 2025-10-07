from django.db import models
from django.utils import timezone
import uuid


class Favorite(models.Model):
    TYPE_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('product', 'Product'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'user_account.User',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Optional relationships - only one should be set based on type
    restaurant = models.ForeignKey(
        'restaurant.Restaurant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='favorites'
    )
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='favorites'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [
            ['user', 'restaurant'],
            ['user', 'product']
        ]

    def __str__(self):
        if self.type == 'restaurant' and self.restaurant:
            return f"{self.user.name} - {self.restaurant.name}"
        elif self.type == 'product' and self.product:
            return f"{self.user.name} - {self.product.name}"
        return f"{self.user.name} - {self.type}"

    def clean(self):
        """Validate that exactly one of restaurant or product is set based on type"""
        from django.core.exceptions import ValidationError
        
        if self.type == 'restaurant' and not self.restaurant:
            raise ValidationError("Restaurant must be set when type is 'restaurant'")
        elif self.type == 'product' and not self.product:
            raise ValidationError("Product must be set when type is 'product'")
        
        if self.type == 'restaurant' and self.product:
            raise ValidationError("Product should not be set when type is 'restaurant'")
        elif self.type == 'product' and self.restaurant:
            raise ValidationError("Restaurant should not be set when type is 'product'")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)