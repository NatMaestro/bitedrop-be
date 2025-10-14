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
        Override save_model to send welcome emails for new users
        """
        is_new_user = not change  # True if creating a new user
        
        # Always use normal Django admin behavior for user creation
        super().save_model(request, obj, form, change)
        
        # Send welcome email for new users
        if is_new_user:
            try:
                # Get the password from the form
                password = form.cleaned_data.get('password1') or form.cleaned_data.get('password')
                
                if password:
                    # Send welcome email with the password
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