from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Schedule, Appointment
from datetime import time
import uuid


class ScheduleModelTest(TestCase):
    def test_schedule_creation(self):
        # Create a Schedule instance for testing
        schedule = Schedule.objects.create(
            weekday=2,  # Set weekday to Tuesday (assuming 0=Monday)
            start_time=time(9, 0),  # Start time at 9:00 AM
            end_time=time(17, 0),   # End time at 5:00 PM
            location='Clinic A',    # Location name
            is_active=True          # Schedule is active
        )
        # Assert the schedule ID is a valid UUID
        self.assertIsInstance(schedule.id, uuid.UUID)
        # Assert the weekday field is set correctly
        self.assertEqual(schedule.weekday, 2)
        # Assert the location field is set correctly
        self.assertEqual(schedule.location, 'Clinic A')
        # Assert the schedule is active
        self.assertTrue(schedule.is_active)


class AppointmentModelTest(TestCase):
    def setUp(self):
        # Create a test user for creating appointments
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a Schedule instance for associating with appointments
        self.schedule = Schedule.objects.create(
            weekday=1,             # Monday (assuming 0=Monday)
            start_time=time(10, 0), # Start time 10:00 AM
            end_time=time(12, 0),   # End time 12:00 PM
            location='Clinic B',    # Location name
            is_active=True          # Schedule is active
        )

    def test_appointment_creation(self):
        # Create an Appointment instance for testing
        appointment = Appointment.objects.create(
            schedule=self.schedule,          # Link to the schedule created in setUp
            appointment_time=time(10, 30),  # Appointment time 10:30 AM
            status='Confirmed',              # Status set to Confirmed
            created_by=self.user,            # Created by the test user
            notes='Bring medical history'   # Additional notes
        )
        # Assert the appointment ID is a valid UUID
        self.assertIsInstance(appointment.id, uuid.UUID)
        # Assert the status field is set correctly
        self.assertEqual(appointment.status, 'Confirmed')
        # Assert the created_by field references the correct user
        self.assertEqual(appointment.created_by.username, 'testuser')
        # Assert the notes field is set correctly
        self.assertEqual(appointment.notes, 'Bring medical history')
        # Assert the appointment's schedule location is correct
        self.assertEqual(appointment.schedule.location, 'Clinic B')
