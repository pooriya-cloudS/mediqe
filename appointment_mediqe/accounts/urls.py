from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register("users", UserViewSet)
router.register("profiles", UserProfileViewSet)

# Include router URLs
urlpatterns = [
    path("", include(router.urls)),
]
