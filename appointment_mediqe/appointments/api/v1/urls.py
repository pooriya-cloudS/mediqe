from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Router setup for ViewSets
router = DefaultRouter()
router.register(r"schedules", ScheduleViewSet, basename="schedule")
router.register(r"appointments", AppointmentViewSet, basename="appointment")

urlpatterns = [
    # Register ViewSets via router
    path("", include(router.urls)),
]
