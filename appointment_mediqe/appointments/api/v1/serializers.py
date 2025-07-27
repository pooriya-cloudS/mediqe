from rest_framework import serializers

from appointments.models import Schedule

# serializer for schedule
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
