from ...models import Schedule, Appointment
from .serializers import (
    ScheduleSerializer,
    AppointmentSerializer,
)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        elif user.role == "doctor":
            return Appointment.objects.filter(doctor=user)
        else:
            return Appointment.objects.filter(patient=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["put"])
    def update_appointment(self, request, pk=None):
        appointment = self.get_object()
        action_type = request.data.get("action")

        if not action_type:
            return Response(
                {"detail": "Missing 'action' field in request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update Status
        elif action_type == "update_status":
            status_value = request.data.get("status")
            if appointment.status == "Cancelled":
                appointment.cancelled_at = timezone.now()
                appointment.save()
            if not status_value:
                return Response(
                    {"detail": "Status field is required for status update."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            appointment.status = status_value
            appointment.save()
            return Response({"detail": "Status updated successfully."})

        else:
            return Response(
                {"detail": f"Unknown action '{action_type}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
