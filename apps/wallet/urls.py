from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletTransactionViewSet

router = DefaultRouter()
router.register(r'wallet-transactions', WalletTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
