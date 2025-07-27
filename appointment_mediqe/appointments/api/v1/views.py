from rest_framework import viewsets
from ...models import Schedule, Appointment
from .serializers import ScheduleSerializer, AppointmentSerializer
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