from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Tạo một Router
router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls