from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Schedule, Appointment
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    ScheduleSerializer,
    AppointmentSerializer,
    AppointmentUpdateSerializer,
    AppointmentStatusSerializer,
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
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


# booking api (create)
class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user who created the appointment
        serializer.save(created_by=self.request.user)


#  Retrieve, Update, or Delete an appointment
class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


#  Cancel an appointment (custom logic)
class AppointmentCancelView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=404)

        # Update status and log cancellation time
        appointment.status = "Cancelled"
        appointment.cancelled_at = timezone.now()
        appointment.save()

        return Response({"message": "Appointment cancelled successfully"}, status=200)


# Reschedule an existing appointment
class AppointmentRescheduleView(generics.UpdateAPIView):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(status="Pending")


# update for status appointment
class AppointmentStatusUpdateView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentStatusSerializer
    permission_classes = [IsAuthenticated]
