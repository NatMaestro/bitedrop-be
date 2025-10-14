from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class Command(BaseCommand):
    help = 'Test email sending with different configurations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='natpaaekow@gmail.com',
            help='Email address to send test email to'
        )
        parser.add_argument(
            '--backend',
            type=str,
            choices=['django', 'smtp_direct', 'gmail_oauth'],
            default='django',
            help='Email backend to test'
        )

    def handle(self, *args, **options):
        email = options['email']
        backend = options['backend']
        
        self.stdout.write(self.style.SUCCESS(f'Testing email to: {email}'))
        self.stdout.write(f'Email backend: {backend}')
        
        # Print current email settings
        self.stdout.write('\n=== Current Email Settings ===')
        self.stdout.write(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        
        # Print environment variables
        self.stdout.write('\n=== Environment Variables ===')
        self.stdout.write(f'EMAIL_HOST_USER env: {os.environ.get("EMAIL_HOST_USER", "NOT SET")}')
        self.stdout.write(f'EMAIL_HOST_PASSWORD env: {"SET" if os.environ.get("EMAIL_HOST_PASSWORD") else "NOT SET"}')
        
        if backend == 'django':
            self.test_django_email(email)
        elif backend == 'smtp_direct':
            self.test_smtp_direct(email)
        elif backend == 'gmail_oauth':
            self.test_gmail_oauth(email)

    def test_django_email(self, email):
        self.stdout.write('\n=== Testing Django Email Backend ===')
        try:
            result = send_mail(
                subject='Test Email from BiteDrop Django',
                message='This is a test email from Django backend.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            if result:
                self.stdout.write(self.style.SUCCESS('✅ Django email sent successfully!'))
            else:
                self.stdout.write(self.style.ERROR('❌ Django email failed to send'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Django email error: {e}'))

    def test_smtp_direct(self, email):
        self.stdout.write('\n=== Testing Direct SMTP Connection ===')
        try:
            # Test SMTP connection
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            if settings.EMAIL_USE_TLS:
                server.starttls()
            
            # Try to login
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            self.stdout.write(self.style.SUCCESS('✅ SMTP login successful!'))
            
            # Create and send email
            msg = MIMEMultipart()
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['To'] = email
            msg['Subject'] = 'Test Email from BiteDrop SMTP'
            
            body = 'This is a test email sent directly via SMTP.'
            msg.attach(MIMEText(body, 'plain'))
            
            text = msg.as_string()
            server.sendmail(settings.DEFAULT_FROM_EMAIL, email, text)
            server.quit()
            
            self.stdout.write(self.style.SUCCESS('✅ Direct SMTP email sent successfully!'))
            
        except smtplib.SMTPAuthenticationError as e:
            self.stdout.write(self.style.ERROR(f'❌ SMTP Authentication Error: {e}'))
            self.stdout.write('💡 Check your Gmail app password and ensure 2FA is enabled')
        except smtplib.SMTPException as e:
            self.stdout.write(self.style.ERROR(f'❌ SMTP Error: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ General Error: {e}'))

    def test_gmail_oauth(self, email):
        self.stdout.write('\n=== Gmail OAuth Configuration ===')
        self.stdout.write('To use Gmail OAuth, you need to:')
        self.stdout.write('1. Create a Google Cloud Project')
        self.stdout.write('2. Enable Gmail API')
        self.stdout.write('3. Create OAuth 2.0 credentials')
        self.stdout.write('4. Install google-auth-oauthlib and google-auth-httplib2')
        self.stdout.write('5. Configure OAuth flow')
        self.stdout.write('\nFor now, stick with app passwords for simplicity.')
