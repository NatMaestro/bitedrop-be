from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    login_view, 
    register_view, 
    refresh_token_view,
    force_password_change_view,
    test_endpoint,
    test_user_creation,
    UserViewSet, 
    StaffViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'staff', StaffViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('token/refresh/', refresh_token_view, name='token_refresh'),
    path('force-password-change/', force_password_change_view, name='force_password_change'),
    path('test/', test_endpoint, name='test'),
    path('test-user-creation/', test_user_creation, name='test_user_creation'),
]
