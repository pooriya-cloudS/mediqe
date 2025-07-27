from rest_framework import viewsets
from ...models import Schedule
from .serializers import ScheduleSerializer
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
        return Schedule.objects.filter(doctor=user)
