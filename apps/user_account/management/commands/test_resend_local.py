"""
Management command to test Resend API locally
Usage: python manage.py test_resend_local
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import render_to_string
import requests
import os


class Command(BaseCommand):
    help = 'Test Resend API email sending locally'

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-key',
            type=str,
            help='Resend API key (optional, can also set EMAIL_HOST_PASSWORD env var)',
        )
        parser.add_argument(
            '--to',
            type=str,
            default='test@example.com',
            help='Email address to send test email to',
        )

    def handle(self, *args, **options):
        # Get API key from argument or environment
        api_key = options['api_key'] or os.environ.get('EMAIL_HOST_PASSWORD')
        
        if not api_key:
            self.stdout.write(
                self.style.ERROR('❌ No Resend API key provided!')
            )
            self.stdout.write(
                'Usage: python manage.py test_resend_local --api-key YOUR_API_KEY --to your@email.com'
            )
            self.stdout.write(
                'Or set EMAIL_HOST_PASSWORD environment variable'
            )
            return

        # Test email data
        test_email = options['to']
        subject = "BiteDrop Test Email - Resend API"
        
        # Create test context
        context = {
            'user_name': 'Test User',
            'user_email': test_email,
            'user_role': 'restaurant_admin',
            'temporary_password': 'TempPass123!',
            'login_url': 'http://localhost:3000/auth',
            'restaurant_name': 'Test Restaurant',
        }
        
        try:
            # Render email templates
            self.stdout.write('📧 Rendering email templates...')
            html_message = render_to_string('emails/welcome_email.html', context)
            plain_message = render_to_string('emails/welcome_email.txt', context)
            self.stdout.write('✅ Templates rendered successfully')
            
            # Send email via Resend API
            self.stdout.write(f'🚀 Sending email to {test_email} via Resend API...')
            
            response = requests.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "from": "BiteDrop <noreply@resend.dev>",
                    "to": [test_email],
                    "subject": subject,
                    "html": html_message,
                    "text": plain_message
                },
                timeout=30
            )
            
            self.stdout.write(f'📊 Response Status: {response.status_code}')
            self.stdout.write(f'📊 Response Body: {response.text}')
            
            if response.status_code == 200:
                result = response.json()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Email sent successfully!')
                )
                self.stdout.write(f'📧 Email ID: {result.get("id", "Unknown")}')
                self.stdout.write(f'📧 To: {test_email}')
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Email sending failed!')
                )
                self.stdout.write(f'Error: {response.text}')
                
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Network error: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Unexpected error: {e}')
            )
            import traceback
            self.stdout.write(f'Traceback: {traceback.format_exc()}')
