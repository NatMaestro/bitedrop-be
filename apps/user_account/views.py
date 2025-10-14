from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    UserListSerializer,
    PasswordChangeSerializer,
    StaffCreateSerializer,
    StaffSerializer,
)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        login(request, user)

        # Generate tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response(
            {
                "access": str(access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "phone": user.phone,
                    "address": user.address,
                    "restaurant": user.restaurant.id if user.restaurant else None,
                    "wallet_balance": user.wallet_balance,
                    "loyalty_points": user.loyalty_points,
                },
            }
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def refresh_token_view(request):
    from rest_framework_simplejwt.tokens import RefreshToken
    
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"error": "Refresh token is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token

        return Response({
            "access": str(access_token),
            "refresh": str(refresh),
        })
    except Exception as e:
        return Response(
            {"error": "Invalid refresh token"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        
        # Super admin can see all users
        if user.role == "admin" or user.is_superuser:
            return User.objects.all()
        
        # Restaurant admin can see users from their restaurant
        elif user.role == "restaurant_admin" and user.restaurant:
            return User.objects.filter(restaurant=user.restaurant)
        
        # Staff can only see themselves
        elif user.role == "staff":
            return User.objects.filter(id=user.id)
        
        # Regular users can only see themselves
        else:
            return User.objects.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        try:
            # Only admin and restaurant_admin can create users
            if request.user.role not in ["admin", "restaurant_admin"]:
                return Response(
                    {"error": "Permission denied"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        
            # Get the data
            data = request.data.copy()
            role = data.get('role')
            
            # For restaurant_admin and staff roles, use auto-generated password
            # For regular users, check if custom password is provided
            if role in ['restaurant_admin', 'staff']:
                from .utils import create_user_with_temporary_password
                
                print(f"DEBUG: Creating {role} user via API")
                try:
                    # Extract restaurant if provided
                    restaurant_id = data.get('restaurant')
                    restaurant = None
                    if restaurant_id:
                        from apps.restaurant.models import Restaurant
                        restaurant = Restaurant.objects.get(id=restaurant_id)
                    
                    # Create user with auto-generated password
                    user, temp_password, email_sent = create_user_with_temporary_password(
                        email=data['email'],
                        name=data['name'],
                        role=role,
                        restaurant=restaurant,
                        phone=data.get('phone'),
                        address=data.get('address'),
                    )
                    
                    # Return user data with email status
                    print(f"DEBUG: User creation completed. Email sent: {email_sent}")
                    serializer = self.get_serializer(user)
                    return Response({
                        **serializer.data,
                        'email_sent': email_sent,
                        'message': f'User created successfully. Welcome email {"sent" if email_sent else "failed to send"}.'
                    }, status=status.HTTP_201_CREATED)
                    
                except Exception as e:
                    error_message = str(e)
                    # Handle specific database errors
                    if "duplicate key value violates unique constraint" in error_message and "email" in error_message:
                        return Response(
                            {"error": "A user with this email address already exists. Please use a different email."}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    return Response(
                        {"error": f"Failed to create user: {error_message}"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            elif role == 'user':
                # For regular users, check if custom password is provided
                custom_password = data.get('password')
                try:
                    if custom_password:
                        # Create user with custom password and send welcome email
                        from .utils import send_welcome_email
                        
                        user = User.objects.create_user(
                            email=data['email'],
                            name=data['name'],
                            password=custom_password,
                            role=role,
                            phone=data.get('phone', ''),
                            address=data.get('address', ''),
                            must_change_password=False,  # Custom password doesn't require change
                        )
                        
                        # Send welcome email with custom password
                        email_sent = send_welcome_email(user, custom_password)
                        
                        serializer = self.get_serializer(user)
                        return Response({
                            **serializer.data,
                            'email_sent': email_sent,
                            'message': f'User created successfully. Welcome email {"sent" if email_sent else "failed to send"}.'
                        }, status=status.HTTP_201_CREATED)
                    else:
                        # No custom password provided, use auto-generated
                        from .utils import create_user_with_temporary_password
                        
                        user, temp_password, email_sent = create_user_with_temporary_password(
                            email=data['email'],
                            name=data['name'],
                            role=role,
                            phone=data.get('phone'),
                            address=data.get('address'),
                        )
                        
                        serializer = self.get_serializer(user)
                        return Response({
                            **serializer.data,
                            'email_sent': email_sent,
                            'message': f'User created successfully. Welcome email {"sent" if email_sent else "failed to send"}.'
                        }, status=status.HTTP_201_CREATED)
                except Exception as e:
                    error_message = str(e)
                    # Handle specific database errors
                    if "duplicate key value violates unique constraint" in error_message and "email" in error_message:
                        return Response(
                            {"error": "A user with this email address already exists. Please use a different email."}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    return Response(
                        {"error": f"Failed to create user: {error_message}"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
            # For regular users, use the default creation process
            return super().create(request, *args, **kwargs)
        except Exception as e:
            import traceback
            print(f"DEBUG: Unexpected error in create method: {str(e)}")
            print(f"DEBUG: Error type: {type(e).__name__}")
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return Response(
                {"error": f"Unexpected error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        current_user = request.user
        
        # Users can only update themselves, unless they're admin
        if current_user.role not in ["admin", "restaurant_admin"] and user.id != current_user.id:
            return Response(
                {"error": "Permission denied"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Only admin can delete users
        if request.user.role != "admin" and not request.user.is_superuser:
            return Response(
                {"error": "Permission denied"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class StaffViewSet(ModelViewSet):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Only restaurant_admin can manage staff
        if user.role == "restaurant_admin" and user.restaurant:
            return User.objects.filter(
                restaurant=user.restaurant, 
                role="staff"
            )
        
        # Admin can see all staff
        elif user.role == "admin" or user.is_superuser:
            return User.objects.filter(role="staff")
        
        return User.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return StaffCreateSerializer
        return StaffSerializer

    def create(self, request, *args, **kwargs):
        # Only restaurant_admin can create staff
        if request.user.role != "restaurant_admin":
            return Response(
                {"error": "Only restaurant admins can create staff members"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not request.user.restaurant:
            return Response(
                {"error": "Restaurant admin must be associated with a restaurant"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff_member = serializer.save()
        
        # Return the created staff member using StaffSerializer
        response_serializer = StaffSerializer(staff_member)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        staff_member = self.get_object()
        current_user = request.user
        
        # Only restaurant_admin can update their staff
        if current_user.role != "restaurant_admin":
            return Response(
                {"error": "Permission denied"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Ensure staff member belongs to the same restaurant
        if staff_member.restaurant != current_user.restaurant:
            return Response(
                {"error": "Cannot update staff from different restaurant"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Handle password update
        password = request.data.get("password")
        if password:
            staff_member.set_password(password)
            staff_member.save()
        
        # Update other fields
        serializer = self.get_serializer(staff_member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        staff_member = self.get_object()
        current_user = request.user
        
        # Only restaurant_admin can delete their staff
        if current_user.role != "restaurant_admin":
            return Response(
                {"error": "Permission denied"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Ensure staff member belongs to the same restaurant
        if staff_member.restaurant != current_user.restaurant:
            return Response(
                {"error": "Cannot delete staff from different restaurant"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        staff_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def force_password_change_view(request):
    """
    Endpoint for forced password change on first login.
    """
    user = request.user
    
    # Check if user actually needs to change password
    if not user.must_change_password:
        return Response(
            {"detail": "Password change not required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        new_password = serializer.validated_data['new_password']
        
        # Update password and clear the flag
        user.set_password(new_password)
        user.must_change_password = False
        user.save()
        
        return Response({
            "detail": "Password changed successfully",
            "must_change_password": False
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)