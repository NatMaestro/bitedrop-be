from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import messages
from .models import User
from .utils import send_welcome_email, create_user_with_temporary_password


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'role', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'name', 'phone']
    ordering = ['-date_joined']
    readonly_fields = ['id', 'date_joined', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('name', 'phone', 'address', 'role', 'restaurant')
        }),
        ('Wallet & Points', {
            'fields': ('wallet_balance', 'loyalty_points')
        }),
        ('Preferences', {
            'fields': ('preferences', 'privacy'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'role'),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to send welcome emails for restaurant_admin and staff roles
        """
        is_new_user = not change  # True if creating a new user
        
        if is_new_user and obj.role in ['restaurant_admin', 'staff']:
            # For restaurant_admin and staff, we need to handle this specially
            # because Django admin creates the user with a password we don't know
            # So we'll delete the user and recreate with our email system
            obj.delete()  # Delete the user created by Django admin
            
            # Recreate using our system that sends emails
            try:
                user, temp_password, email_sent = create_user_with_temporary_password(
                    email=form.cleaned_data['email'],
                    name=form.cleaned_data['name'],
                    role=form.cleaned_data['role'],
                    restaurant=getattr(obj, 'restaurant', None),
                    phone=getattr(obj, 'phone', ''),
                    address=getattr(obj, 'address', ''),
                )
                
                if email_sent:
                    messages.success(request, f'User created successfully. Welcome email sent to {user.email}.')
                else:
                    messages.warning(request, f'User created successfully but welcome email failed to send to {user.email}.')
                    
            except Exception as e:
                messages.error(request, f'Error creating user: {str(e)}')
                # Recreate the user without email sending as fallback
                super().save_model(request, obj, form, change)
        else:
            # For regular users or existing users, use normal Django admin behavior
            super().save_model(request, obj, form, change)
            
            # Send welcome email for new regular users if they have a custom password
            if is_new_user and obj.role == 'user' and form.cleaned_data.get('password1'):
                try:
                    email_sent = send_welcome_email(obj, form.cleaned_data['password1'])
                    if email_sent:
                        messages.success(request, f'User created successfully. Welcome email sent to {obj.email}.')
                    else:
                        messages.warning(request, f'User created successfully but welcome email failed to send to {obj.email}.')
                except Exception as e:
                    messages.warning(request, f'User created but email sending failed: {str(e)}')