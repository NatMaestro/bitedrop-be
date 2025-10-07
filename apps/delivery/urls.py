from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeliveryZoneViewSet

router = DefaultRouter()
router.register(r'delivery-zones', DeliveryZoneViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
