from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Router setup for ViewSets
router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    # Register ViewSets via router
    path('', include(router.urls)),

    # Extra actions using CBV (not ViewSet based)
    path('appointment/create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointment/<uuid:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointment/<uuid:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),
    path('appointment/<uuid:pk>/reschedule/', AppointmentRescheduleView.as_view(), name='appointment-reschedule'),
    path('appointment/<uuid:pk>/status/', AppointmentStatusUpdateView.as_view(), name='appointment-status-update'),
]
