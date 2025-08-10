from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import action
from django.utils import timezone
from ...models import Schedule, Appointment
from .permissions import *
from .serializers import ScheduleSerializer, AppointmentSerializer


@extend_schema(
    tags=["Schedule"],
    summary="Manage Doctor Schedules",
    description="""
    This API allows you to list, create, update, and delete doctor schedules.
    - Staff users can see and manage all schedules.
    - Doctors can only see and manage their own schedules.
    """,
    responses={
        200: ScheduleSerializer(many=True),
        201: ScheduleSerializer,
        204: OpenApiResponse(description="Deleted successfully"),
    },
)
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated, AccessViewSchedule]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Schedule.objects.all()
        return Schedule.objects.filter(doctor=user)


@extend_schema(
    tags=["Appointment"],
    summary="Manage Appointments",
    description="""
    This API allows listing, creating, updating, and deleting appointments.
    - Staff users can see all appointments.
    - Doctors can see only their appointments.
    - Patients can see only their appointments.

    There's a custom action to update appointment status that requires sending
    'action':'update_status' along with the 'status' field.
    """,
    responses={
        200: AppointmentSerializer(many=True),
        201: AppointmentSerializer,
        204: OpenApiResponse(description="Deleted successfully"),
    },
)
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, AccessViewAppointment]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        elif hasattr(user, "role") and user.role == "doctor":
            return Appointment.objects.filter(doctor=user)
        else:
            return Appointment.objects.filter(patient=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(
        summary="Update Appointment Status",
        description="To change the status, send 'action'='update_status' and the 'status' field.",
        responses={200: OpenApiResponse(description="Status updated successfully")},
    )
    @action(detail=True, methods=["put"])
    def update_appointment(self, request, pk=None):
        appointment = self.get_object()
        self.check_object_permissions(request, appointment)

        action_type = request.data.get("action")
        if not action_type:
            return Response(
                {"detail": "Missing 'action' field in request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if action_type == "update_status":
            status_value = request.data.get("status")
            if not status_value:
                return Response(
                    {"detail": "Status field is required for status update."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if appointment.status == "Cancelled" and status_value != "Cancelled":
                appointment.cancelled_at = None

            if status_value == "Cancelled" and appointment.status != "Cancelled":
                appointment.cancelled_at = timezone.now()

            appointment.status = status_value
            appointment.save()
            return Response({"detail": "Status updated successfully."})

        return Response(
            {"detail": f"Unknown action '{action_type}'."},
            status=status.HTTP_400_BAD_REQUEST,
        )
