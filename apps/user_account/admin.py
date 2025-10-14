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
        Override save_model to send welcome emails for new users and handle restaurant roles
        """
        is_new_user = not change  # True if creating a new user
        
        if is_new_user and obj.role in ['restaurant_admin', 'staff']:
            # For restaurant roles, use the proper function with must_change_password=True
            try:
                password = form.cleaned_data.get('password1') or form.cleaned_data.get('password')
                if not password:
                    # Generate a temporary password
                    from .utils import create_user_with_temporary_password
                    user, temp_password, email_sent = create_user_with_temporary_password(
                        email=obj.email,
                        name=obj.name,
                        role=obj.role,
                        restaurant=obj.restaurant,
                        phone=obj.phone,
                        address=obj.address,
                    )
                    messages.success(request, f'Restaurant {obj.role} created successfully. Welcome email {"sent" if email_sent else "failed to send"} to {obj.email}.')
                    return  # Exit early, user already created
                else:
                    # User provided a password, but we still need to set must_change_password=True
                    super().save_model(request, obj, form, change)
                    obj.must_change_password = True
                    obj.save()
                    
                    # Send welcome email
                    email_sent = send_welcome_email(obj, password)
                    if email_sent:
                        messages.success(request, f'Restaurant {obj.role} created successfully. Welcome email sent to {obj.email}.')
                    else:
                        messages.warning(request, f'Restaurant {obj.role} created successfully but welcome email failed to send to {obj.email}.')
                        
            except Exception as e:
                messages.error(request, f'Failed to create restaurant {obj.role}: {str(e)}')
        else:
            # Normal user creation/update
            super().save_model(request, obj, form, change)
            
            # Send welcome email for new users with custom passwords
            if is_new_user:
                try:
                    password = form.cleaned_data.get('password1') or form.cleaned_data.get('password')
                    if password:
                        email_sent = send_welcome_email(obj, password)
                        if email_sent:
                            messages.success(request, f'User created successfully. Welcome email sent to {obj.email}.')
                        else:
                            messages.warning(request, f'User created successfully but welcome email failed to send to {obj.email}.')
                    else:
                        messages.success(request, f'User created successfully. No password provided for email.')
                        
                except Exception as e:
                    messages.warning(request, f'User created successfully but email sending failed: {str(e)}')
            else:
                messages.success(request, f'User updated successfully.')