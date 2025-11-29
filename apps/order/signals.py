from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from apps.notification.models import Notification


@receiver(post_save, sender=Order)
def notify_restaurant_on_order(sender, instance, created, **kwargs):
    """
    Notify restaurant admins and staff when a new order is created.
    This enables multi-tenant order notifications.
    """
    if created and instance.status == 'pending':
        # Get unique restaurants from order items
        restaurants = set()
        for item in instance.items.all():
            if item.product.restaurant:
                restaurants.add(item.product.restaurant)
        
        # Notify each restaurant's admin and staff
        for restaurant in restaurants:
            # Notify restaurant admin
            restaurant_admin = restaurant.users.filter(role='restaurant_admin').first()
            if restaurant_admin:
                Notification.objects.create(
                    user=restaurant_admin,
                    title=f"New Order #{str(instance.id)[:8]}",
                    message=f"You have a new order from {instance.user.name}. Total: ${instance.total}",
                    type='order_update',
                    order=instance
                )
            
            # Notify all staff members
            staff_members = restaurant.users.filter(role='staff')
            for staff in staff_members:
                Notification.objects.create(
                    user=staff,
                    title=f"New Order #{str(instance.id)[:8]}",
                    message=f"New order from {instance.user.name}. Total: ${instance.total}",
                    type='order_update',
                    order=instance
                )


@receiver(post_save, sender=Order)
def notify_customer_on_order_update(sender, instance, created, **kwargs):
    """
    Notify customer when their order status changes.
    Note: This will notify on every save. For production, consider using
    django-model-utils or tracking previous state to avoid duplicate notifications.
    """
    if not created:  # Only notify on updates, not creation
        # Notify customer of status updates
        status_messages = {
            'confirmed': 'Your order has been confirmed and is being prepared.',
            'preparing': 'Your order is being prepared by the restaurant.',
            'ready': 'Your order is ready for pickup/delivery!',
            'delivering': 'Your order is out for delivery!',
            'delivered': 'Your order has been delivered. Enjoy your meal!',
            'cancelled': 'Your order has been cancelled.',
        }
        
        # Only notify for status changes (not pending, as that's the initial state)
        if instance.status != 'pending':
            message = status_messages.get(
                instance.status,
                f'Your order status has been updated to {instance.status}.'
            )
            
            Notification.objects.create(
                user=instance.user,
                title=f"Order #{str(instance.id)[:8]} Update",
                message=message,
                type='order_update',
                order=instance
            )

