from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Router setup for ViewSets
router = DefaultRouter()
router.register(r"schedules", ScheduleViewSet, basename="schedule")
router.register(r"appointments", AppointmentViewSet, basename="appointment")

urlpatterns = [
    # Register ViewSets via router
    path("", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
