# Django
from django.urls import path
# Rest
from rest_framework.routers import DefaultRouter
# Local
from .views import TransactionViewSet


router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
