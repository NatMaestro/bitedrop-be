from django.core.management.base import BaseCommand
from apps.user_account.models import User
from apps.restaurant.models import Restaurant


class Command(BaseCommand):
    help = 'Assign restaurants to restaurant admin users'

    def handle(self, *args, **options):
        # Get all restaurant admin users without a restaurant
        restaurant_admins = User.objects.filter(
            role='restaurant_admin',
            restaurant__isnull=True
        )
        
        # Get all restaurants
        restaurants = Restaurant.objects.all()
        
        if not restaurants.exists():
            self.stdout.write(
                self.style.ERROR('No restaurants found in the database')
            )
            return
        
        if not restaurant_admins.exists():
            self.stdout.write(
                self.style.WARNING('No restaurant admin users found without restaurants')
            )
            return
        
        # Assign restaurants to restaurant admins
        for i, admin in enumerate(restaurant_admins):
            # Cycle through restaurants if there are more admins than restaurants
            restaurant = restaurants[i % len(restaurants)]
            admin.restaurant = restaurant
            admin.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Assigned restaurant "{restaurant.name}" to user "{admin.name}" ({admin.email})'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully assigned restaurants to {restaurant_admins.count()} users'
            )
        )
