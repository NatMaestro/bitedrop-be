from django.db import models
from django.utils import timezone
import uuid


class Notification(models.Model):
    TYPE_CHOICES = [
        ('welcome', 'Welcome'),
        ('order_update', 'Order Update'),
        ('promotion', 'Promotion'),
        ('payment', 'Payment'),
        ('delivery', 'Delivery'),
        ('system', 'System'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'user_account.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    
    # Optional relationships
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    discount = models.ForeignKey(
        'discount.Discount',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.name} - {self.title}"

    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])

    @classmethod
    def create_order_notification(cls, user, order, title, message):
        """Create an order-related notification"""
        return cls.objects.create(
            user=user,
            title=title,
            message=message,
            type='order_update',
            order=order
        )

    @classmethod
    def create_promotion_notification(cls, user, discount, title, message):
        """Create a promotion-related notification"""
        return cls.objects.create(
            user=user,
            title=title,
            message=message,
            type='promotion',
            discount=discount
        )