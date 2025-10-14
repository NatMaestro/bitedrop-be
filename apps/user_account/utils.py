import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def generate_secure_password(length=12):
    """
    Generate a secure random password with letters, digits, and special characters.
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def send_welcome_email(user, temporary_password):
    """
    Send welcome email to newly created restaurant admin or staff.
    """
    subject = f"Welcome to BiteDrop - Your Account Details"
    
    # Email context
    # Get frontend URL from settings or use a default
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    
    context = {
        'user_name': user.name,
        'user_email': user.email,
        'user_role': user.get_role_display(),
        'temporary_password': temporary_password,
        'login_url': f"{frontend_url}/auth",
        'restaurant_name': user.restaurant.name if user.restaurant else None,
    }
    
    # Render HTML email template
    html_message = render_to_string('emails/welcome_email.html', context)
    plain_message = render_to_string('emails/welcome_email.txt', context)
    
    try:
        print(f"DEBUG: Attempting to send email to {user.email}")
        print(f"DEBUG: Email backend: {settings.EMAIL_BACKEND}")
        print(f"DEBUG: Email host: {settings.EMAIL_HOST}")
        print(f"DEBUG: Email port: {settings.EMAIL_PORT}")
        print(f"DEBUG: Email use TLS: {settings.EMAIL_USE_TLS}")
        print(f"DEBUG: From email: {settings.DEFAULT_FROM_EMAIL}")
        print(f"DEBUG: Email user configured: {'Yes' if settings.EMAIL_HOST_USER else 'No'}")
        print(f"DEBUG: Email password configured: {'Yes' if settings.EMAIL_HOST_PASSWORD else 'No'}")
        
        # Check if we have email credentials
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            print("WARNING: No email credentials configured, email will not be sent")
            return False
        
        # Try to send email with detailed error handling
        result = send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,  # Changed back to False to see actual errors
        )
        print(f"DEBUG: Email send result: {result}")
        
        if result:
            print(f"✅ Welcome email sent successfully to {user.email}")
            return True
        else:
            print(f"❌ Email send returned 0 (no emails sent)")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send welcome email to {user.email}: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Provide specific error guidance
        if "authentication" in str(e).lower() or "535" in str(e):
            print("💡 Authentication error - check your Resend API key")
            print("💡 Make sure your API key is correct and starts with 're_'")
        elif "domain" in str(e).lower() or "450" in str(e):
            print("💡 Domain verification error - check your DEFAULT_FROM_EMAIL")
            print("💡 Use noreply@resend.dev or verify your custom domain in Resend")
        elif "connection" in str(e).lower() or "timeout" in str(e).lower():
            print("💡 Connection error - check your internet connection and Resend SMTP settings")
            print("💡 Verify EMAIL_HOST=smtp.resend.com and EMAIL_PORT=587")
        elif "tls" in str(e).lower():
            print("💡 TLS error - make sure EMAIL_USE_TLS=True")
        else:
            print(f"💡 Unknown error - check Resend dashboard for more details")
        
        return False


def create_user_with_temporary_password(email, name, role, restaurant=None, phone=None, address=None):
    """
    Create a user with a temporary password and send welcome email.
    Returns the created user and the temporary password.
    """
    from .models import User
    
    # Generate temporary password
    temporary_password = generate_secure_password()
    
    # Create user with must_change_password flag
    user = User.objects.create_user(
        email=email,
        name=name,
        password=temporary_password,
        role=role,
        restaurant=restaurant,
        phone=phone or "",
        address=address or "",
        must_change_password=True,  # Force password change on first login
    )
    
    # Send welcome email
    email_sent = send_welcome_email(user, temporary_password)
    
    return user, temporary_password, email_sent
