"""
Management command to fix user's must_change_password flag
Usage: python manage.py fix_user_password --email user@example.com
"""
from django.core.management.base import BaseCommand
from apps.user_account.models import User


class Command(BaseCommand):
    help = 'Set must_change_password=True for a user'

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
            self.stdout.write(f"🔒 Current must_change_password: {user.must_change_password}")
            
            # Set the flag to True
            user.must_change_password = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Updated must_change_password to True for {email}')
            )
            
            # Verify the change
            user.refresh_from_db()
            self.stdout.write(f"🔒 New must_change_password: {user.must_change_password}")
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ User with email {email} not found!')
            )


