from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Test Resend email configuration on Render.com'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='Email address to send test email to'
        )

    def handle(self, *args, **options):
        email = options['email']
        
        self.stdout.write(self.style.SUCCESS(f'Testing Resend email to: {email}'))
        
        # Print all email settings
        self.stdout.write('\n=== Email Configuration ===')
        self.stdout.write(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'EMAIL_HOST_PASSWORD configured: {"Yes" if settings.EMAIL_HOST_PASSWORD else "No"}')
        
        # Print environment variables
        self.stdout.write('\n=== Environment Variables ===')
        self.stdout.write(f'EMAIL_HOST env: {os.environ.get("EMAIL_HOST", "NOT SET")}')
        self.stdout.write(f'EMAIL_HOST_USER env: {os.environ.get("EMAIL_HOST_USER", "NOT SET")}')
        self.stdout.write(f'EMAIL_HOST_PASSWORD env: {"SET" if os.environ.get("EMAIL_HOST_PASSWORD") else "NOT SET"}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL env: {os.environ.get("DEFAULT_FROM_EMAIL", "NOT SET")}')
        
        # Test email sending
        self.stdout.write('\n=== Testing Email Send ===')
        try:
            result = send_mail(
                subject='Test Email from BiteDrop (Resend)',
                message='This is a test email from BiteDrop using Resend.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            if result:
                self.stdout.write(self.style.SUCCESS('✅ Email sent successfully!'))
                self.stdout.write(f'Result: {result} emails sent')
            else:
                self.stdout.write(self.style.ERROR('❌ Email failed to send'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Email error: {e}'))
            self.stdout.write(f'Error type: {type(e).__name__}')
            
            # Provide specific guidance
            error_str = str(e).lower()
            if "authentication" in error_str or "535" in error_str:
                self.stdout.write('💡 Authentication error - check your Resend API key')
            elif "domain" in error_str or "450" in error_str:
                self.stdout.write('💡 Domain error - use noreply@resend.dev for DEFAULT_FROM_EMAIL')
            elif "connection" in error_str:
                self.stdout.write('💡 Connection error - check EMAIL_HOST and EMAIL_PORT')
            else:
                self.stdout.write(f'💡 Check Resend dashboard for more details')
