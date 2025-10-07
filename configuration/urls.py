"""
URL configuration for configuration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="BiteDrop API",
        default_version='v1',
        description="""
        # BiteDrop Food Delivery Platform API
        
        Welcome to the BiteDrop API documentation! This API powers our food delivery platform with comprehensive features for restaurants, customers, and delivery management.
        
        ## Features
        - 🍕 **Restaurant Management** - Complete restaurant profiles, menus, and operations
        - 🛒 **Order Management** - End-to-end order processing and tracking
        - 💰 **Wallet System** - Digital wallet with loyalty points and transactions
        - ⭐ **Reviews & Ratings** - Customer feedback and rating system
        - 🎯 **Discounts & Promotions** - Flexible discount system for restaurants and products
        - 📱 **Notifications** - Real-time notifications for order updates
        - 🚚 **Delivery Management** - Delivery zones and tracking
        - 💳 **Payment Integration** - Multiple payment methods support
        
        ## Authentication
        This API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:
        ```
        Authorization: Bearer <your-jwt-token>
        ```
        
        ## Getting Started
        1. Register a new user account
        2. Login to get your JWT token
        3. Use the token to access protected endpoints
        4. Explore restaurants, place orders, and manage your account
        
        ## Support
        For API support, please contact our development team.
        """,
        terms_of_service="https://www.bitedrop.com/terms/",
        contact=openapi.Contact(email="api@bitedrop.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # API Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API Endpoints
    path('api/users/', include('apps.user_account.urls')),
    path('api/', include('apps.restaurant.urls')),
    path('api/', include('apps.category.urls')),
    path('api/', include('apps.product.urls')),
    path('api/', include('apps.order.urls')),
    path('api/', include('apps.discount.urls')),
    path('api/', include('apps.favorite.urls')),
    path('api/', include('apps.wallet.urls')),
    path('api/', include('apps.notification.urls')),
    path('api/', include('apps.review.urls')),
    path('api/', include('apps.delivery.urls')),
    path('api/', include('apps.payment.urls')),
]
