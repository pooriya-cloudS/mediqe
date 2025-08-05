from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Schedule, Appointment
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    ScheduleSerializer,
    AppointmentSerializer,
)
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


# ViewSet for Schedule providing full CRUD functionality
# Only authenticated users can access these endpoints
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Limit the queryset to schedules belonging to the logged-in user (doctor)
        user = self.request.user
        if user.is_staff:
            return Schedule.objects.all()
        else:
            return Schedule.objects.filter(doctor=user)


# ViewSet for Appointment providing full CRUD functionality
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # cancel appointment
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        if appointment.status == "Cancelled":
            return Response(
                {"detail": "Appointment already cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = "Cancelled"
        appointment.cancelled_at = timezone.now()
        appointment.save()
        return Response({"detail": "Appointment cancelled successfully."})

    # reschedule appointment
    @action(detail=True, methods=["post"])
    def reschedule(self, request, pk=None):
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(status="Pending")
        return Response(serializer.data)

    # update status appointment
    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        appointment = self.get_object()
        status_value = request.data.get("status")
        if not status_value:
            return Response(
                {"detail": "Status field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = status_value
        appointment.save()
        return Response({"detail": "Status updated successfully."})
