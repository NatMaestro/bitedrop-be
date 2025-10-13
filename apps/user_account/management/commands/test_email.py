"""
Django management command to test email functionality
Usage: python manage.py test_email
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test email to',
            default='natpaaekow@gmail.com'
        )

    def handle(self, *args, **options):
        recipient_email = options['email']
        
        self.stdout.write("Testing email configuration...")
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write("-" * 50)
        
        try:
            result = send_mail(
                subject="Test Email from BiteDrop Django App",
                message="Hello! This is a test email from your BiteDrop Django application. If you receive this, your email configuration is working correctly!",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Email sent successfully! Result: {result}')
            )
            self.stdout.write(f"Check {recipient_email} for the test message.")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending email: {e}')
            )
            self.stdout.write("Please check your email configuration and try again.")
