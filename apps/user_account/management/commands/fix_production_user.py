"""
Management command to fix user's must_change_password flag in production
Usage: python manage.py fix_production_user --email user@example.com
"""
from django.core.management.base import BaseCommand
from apps.user_account.models import User


class Command(BaseCommand):
    help = 'Set must_change_password=True for a user in production'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Email address of the user to fix',
        )

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            user = User.objects.get(email=email)
            
            self.stdout.write(f"📧 User: {user.email}")
            self.stdout.write(f"👤 Name: {user.name}")
            self.stdout.write(f"🎭 Role: {user.role}")
            self.stdout.write(f"🔒 Current must_change_password: {user.must_change_password}")
            
            if user.must_change_password:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ User {email} already has must_change_password=True')
                )
                return
            
            # Set the flag to True
            user.must_change_password = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Updated must_change_password to True for {email}')
            )
            
            # Verify the change
            user.refresh_from_db()
            self.stdout.write(f"🔒 New must_change_password: {user.must_change_password}")
            
            # Also check if this is a restaurant role that should have the flag
            if user.role in ['restaurant_admin', 'staff']:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ User {email} is a {user.role} and now requires password change on next login')
                )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ User with email {email} not found!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error fixing user: {str(e)}')
            )


