import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests


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
    try:
        print(f"DEBUG: Starting email sending for user: {user.email}")
        subject = f"Welcome to BiteDrop - Your Account Details"
        
        # Email context
        # Get frontend URL from settings or use a default
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        
        context = {
            'user_name': user.name,
            'user_email': user.email,
            'user_role': user.role,
            'temporary_password': temporary_password,
            'login_url': f"{frontend_url}/auth",
            'restaurant_name': user.restaurant.name if user.restaurant and hasattr(user.restaurant, 'name') else None,
        }
        
        # Render HTML email template
        print("DEBUG: Rendering email templates...")
        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = render_to_string('emails/welcome_email.txt', context)
        print("DEBUG: Email templates rendered successfully")
        
        # Get Resend API key from settings
        resend_api_key = getattr(settings, 'EMAIL_HOST_PASSWORD', None)
        if not resend_api_key:
            print("WARNING: No Resend API key configured (EMAIL_HOST_PASSWORD), email will not be sent")
            return False
            
        print("DEBUG: Using Resend API to send email...")
        
        # Send email using Resend API
        response = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {resend_api_key}"},
            json={
                "from": "BiteDrop <noreply@resend.dev>",
                "to": [user.email],
                "subject": subject,
                "html": html_message,
                "text": plain_message
            },
            timeout=30
        )
        
        print(f"DEBUG: Resend API response status: {response.status_code}")
        print(f"DEBUG: Resend API response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Welcome email sent successfully to {user.email}")
            print(f"DEBUG: Email ID: {result.get('id', 'Unknown')}")
            return True
        else:
            print(f"❌ Resend API error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error sending email to {user.email}: {e}")
        return False
    except Exception as e:
        print(f"DEBUG: Email sending failed with exception: {str(e)}")
        import traceback
        print(f"DEBUG: Email sending traceback: {traceback.format_exc()}")
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
    print(f"DEBUG: Creating user {email} with must_change_password=True")
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
    print(f"DEBUG: User created with must_change_password: {user.must_change_password}")
    
    # Send welcome email
    email_sent = send_welcome_email(user, temporary_password)
    
    return user, temporary_password, email_sent
