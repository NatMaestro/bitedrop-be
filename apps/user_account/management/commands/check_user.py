"""
Management command to check user details
Usage: python manage.py check_user --email user@example.com
"""
from django.core.management.base import BaseCommand
from apps.user_account.models import User


class Command(BaseCommand):
    help = 'Check user details and must_change_password status'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Email address of the user to check',
        )

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            user = User.objects.get(email=email)
            
            self.stdout.write(f"📧 User: {user.email}")
            self.stdout.write(f"👤 Name: {user.name}")
            self.stdout.write(f"🎭 Role: {user.role}")
            self.stdout.write(f"🏪 Restaurant: {user.restaurant}")
            self.stdout.write(f"🔒 Must Change Password: {user.must_change_password}")
            self.stdout.write(f"✅ Is Active: {user.is_active}")
            self.stdout.write(f"📅 Date Joined: {user.date_joined}")
            self.stdout.write(f"🕒 Last Login: {user.last_login}")
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ User with email {email} not found!')
            )
