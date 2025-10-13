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
    context = {
        'user_name': user.name,
        'user_email': user.email,
        'user_role': user.get_role_display(),
        'temporary_password': temporary_password,
        'login_url': f"{settings.FRONTEND_URL}/auth",
        'restaurant_name': user.restaurant.name if user.restaurant else None,
    }
    
    # Render HTML email template
    html_message = render_to_string('emails/welcome_email.html', context)
    plain_message = render_to_string('emails/welcome_email.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send welcome email to {user.email}: {e}")
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
