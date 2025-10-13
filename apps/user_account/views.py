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
        # Only admin and restaurant_admin can create users
        if request.user.role not in ["admin", "restaurant_admin"]:
            return Response(
                {"error": "Permission denied"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

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