from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    authentication_classes = []  # 👈 make registration public
    permission_classes = []      # 👈 no auth required

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Create a new user account and receive JWT tokens for authentication",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='User data'),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(description="Bad request - validation errors")
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Generate JWT tokens for the newly created user
            refresh = RefreshToken.for_user(user=serializer.instance)

            return Response({
                "message": "Registration successful",
                "user": serializer.data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get current user profile",
        operation_description="Retrieve the authenticated user's profile information",
        responses={
            200: UserSerializer,
            401: openapi.Response(description="Unauthorized - authentication required")
        },
        tags=['User Profile']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update current user profile",
        operation_description="Update the authenticated user's profile information",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: openapi.Response(description="Bad request - validation errors"),
            401: openapi.Response(description="Unauthorized - authentication required")
        },
        tags=['User Profile']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update current user profile",
        operation_description="Partially update the authenticated user's profile information",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: openapi.Response(description="Bad request - validation errors"),
            401: openapi.Response(description="Unauthorized - authentication required")
        },
        tags=['User Profile']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="User login",
        operation_description="Authenticate user credentials and receive JWT tokens",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='User data'),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(description="Bad request - invalid credentials")
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": "Login successful",
                "user": {k: v for k, v in serializer.data.items() if k not in ["refresh", "access"]},
                "tokens": {
                    "refresh": serializer.data["refresh"],
                    "access": serializer.data["access"],
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'email', 'date_joined', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            # Only staff can list all users
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'create':
            # Anyone can register (handled by RegisterView)
            permission_classes = [permissions.AllowAny]
        else:
            # Users can view/edit their own profile, staff can view/edit any
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Return users based on permissions"""
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            # Non-staff users can only see their own profile
            return User.objects.filter(id=self.request.user.id)

    @swagger_auto_schema(
        operation_summary="List all users",
        operation_description="Get a list of all users (admin only)",
        responses={
            200: UserSerializer(many=True),
            403: openapi.Response(description="Forbidden - admin access required")
        },
        tags=['User Management']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get user details",
        operation_description="Get details of a specific user",
        responses={
            200: UserSerializer,
            404: openapi.Response(description="User not found"),
            403: openapi.Response(description="Forbidden - insufficient permissions")
        },
        tags=['User Management']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update user",
        operation_description="Update user information",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: openapi.Response(description="Bad request - validation errors"),
            403: openapi.Response(description="Forbidden - insufficient permissions")
        },
        tags=['User Management']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update user",
        operation_description="Partially update user information",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: openapi.Response(description="Bad request - validation errors"),
            403: openapi.Response(description="Forbidden - insufficient permissions")
        },
        tags=['User Management']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete user",
        operation_description="Delete a user account (admin only)",
        responses={
            204: openapi.Response(description="User deleted successfully"),
            403: openapi.Response(description="Forbidden - admin access required")
        },
        tags=['User Management']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
