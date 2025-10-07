from django.db import models
from django.utils import timezone
import uuid


class PaymentMethod(models.Model):
    TYPE_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('card', 'Credit/Debit Card'),
        ('wallet', 'BiteDrop Wallet'),
        ('cash', 'Cash on Delivery'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    supported_networks = models.JSONField(default=list, blank=True)  # List of supported networks
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name