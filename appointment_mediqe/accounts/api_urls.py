from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet
from django.urls import path, include
from .views import RegisterAPIView, LoginAPIView


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", UserProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),  # /api/users/ , /api/profiles/
    path("register/", RegisterAPIView.as_view(), name="register_api"),
    path("login/", LoginAPIView.as_view(), name="login_api"),
]
