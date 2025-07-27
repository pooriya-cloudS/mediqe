from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'schedule', ScheduleViewSet, basename='schedule')
router.register(r'appointment', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
]
