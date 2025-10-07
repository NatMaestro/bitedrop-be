from django.db import models
from django.utils import timezone
import uuid


class WalletTransaction(models.Model):
    TYPE_CHOICES = [
        ('earned', 'Earned'),
        ('redeemed', 'Redeemed'),
        ('bonus', 'Bonus'),
        ('refund', 'Refund'),
        ('top_up', 'Top Up'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'user_account.User',
        on_delete=models.CASCADE,
        related_name='wallet_transactions'
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Can be positive or negative
    points = models.IntegerField()  # Loyalty points (can be positive or negative)
    description = models.TextField()
    
    # Optional relationship to order
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wallet_transactions'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.name} - {self.type} - {self.amount}"

    def save(self, *args, **kwargs):
        """Update user's wallet balance and loyalty points when transaction is saved"""
        super().save(*args, **kwargs)
        
        # Update user's wallet balance and loyalty points
        user = self.user
        user.wallet_balance += self.amount
        user.loyalty_points += self.points
        
        # Ensure non-negative values
        if user.wallet_balance < 0:
            user.wallet_balance = 0
        if user.loyalty_points < 0:
            user.loyalty_points = 0
            
        user.save(update_fields=['wallet_balance', 'loyalty_points'])