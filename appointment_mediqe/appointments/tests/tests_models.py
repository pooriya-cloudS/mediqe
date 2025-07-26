from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Schedule, Appointment
from datetime import time
import uuid

class ScheduleModelTest(TestCase):
    def test_schedule_creation(self):
        schedule = Schedule.objects.create(
            weekday=2,
            start_time=time(9, 0),
            end_time=time(17, 0),
            location='Clinic A',
            is_active=True
        )
        self.assertIsInstance(schedule.id, uuid.UUID)
        self.assertEqual(schedule.weekday, 2)
        self.assertEqual(schedule.location, 'Clinic A')
        self.assertTrue(schedule.is_active)

class AppointmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.schedule = Schedule.objects.create(
            weekday=1,
            start_time=time(10, 0),
            end_time=time(12, 0),
            location='Clinic B',
            is_active=True
        )

    def test_appointment_creation(self):
        appointment = Appointment.objects.create(
            schedule=self.schedule,
            appointment_time=time(10, 30),
            status='Confirmed',
            created_by=self.user,
            notes='Bring medical history'
        )
        self.assertIsInstance(appointment.id, uuid.UUID)
        self.assertEqual(appointment.status, 'Confirmed')
        self.assertEqual(appointment.created_by.username, 'testuser')
        self.assertEqual(appointment.notes, 'Bring medical history')
        self.assertEqual(appointment.schedule.location, 'Clinic B')