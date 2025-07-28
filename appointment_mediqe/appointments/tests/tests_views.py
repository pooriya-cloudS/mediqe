from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIRequestFactory
from appointments.api.v1.serializers import AppointmentSerializer
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import time
from django.utils import timezone
from appointments.models import Appointment, Schedule
from django.contrib.auth import get_user_model

User = get_user_model()

class AppointmentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create user and login
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Create schedule (adapted to new model)
        self.schedule = Schedule.objects.create(
            doctor=self.user,
            weekday=0,  # Monday
            start_time=time(9, 0),
            end_time=time(12, 0),
            location="Clinic A",
            is_active=True,
        )

        # Create appointment (adapted to new model)
        self.appointment = Appointment.objects.create(
            doctor=self.user,
            patient=self.user,
            schedule=self.schedule,
            appointment_time=time(10, 0),
            status='Pending',
            created_by=self.user
        )

    # ✅ Test appointment creation
    def test_create_appointment(self):
        url = reverse('appointment-create')
        data = {
            'doctor': self.user.id,
            'patient': self.user.id,
            'schedule': str(self.schedule.id),
            'appointment_time': '10:30:00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'Pending')

    # ✅ Retrieve appointment
    def test_retrieve_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.appointment.pk))

    # ✅ Update appointment
    def test_update_appointment_time(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})
        response = self.client.patch(url, {'appointment_time': '11:00:00'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(str(self.appointment.appointment_time), '11:00:00')

    # ✅ Delete appointment
    def test_delete_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Appointment.objects.filter(pk=self.appointment.pk).exists())

    # ✅ Cancel appointment
    def test_cancel_appointment(self):
        url = reverse('appointment-cancel', kwargs={'pk': self.appointment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'Cancelled')
        self.assertIsNotNone(self.appointment.cancelled_at)

    # ✅ Reschedule appointment
    def test_reschedule_appointment(self):
        url = reverse('appointment-reschedule', kwargs={'pk': self.appointment.pk})
        data = {
            'appointment_time': '11:30:00',
            'schedule': str(self.schedule.id)
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(str(self.appointment.appointment_time), '11:30:00')
        self.assertEqual(self.appointment.status, 'Pending')

    # ✅ Update appointment status
    def test_update_appointment_status(self):
        url = reverse('appointment-status-update', kwargs={'pk': self.appointment.pk})
        data = {'status': 'Completed'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'Completed')

class ScheduleCRUDTestCase(APITestCase):

    def setUp(self):
        # Create a doctor user
        self.doctor = User.objects.create_user(username="doctor1", password="pass123")
        self.client.login(username="doctor1", password="pass123")
        self.list_url = reverse("schedule-list")

        # Sample data for creating a Schedule
        self.schedule_data = {
            "doctor": self.doctor.id,
            "weekday": 0,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "location": "Clinic A",
            "is_active": True,
        }

    def test_create_schedule(self):
        # Test creating a new schedule entry
        response = self.client.post(self.list_url, self.schedule_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(Schedule.objects.get().location, "Clinic A")

    def test_read_schedule_list(self):
        # Create a schedule to read
        Schedule.objects.create(
            doctor=self.doctor,
            weekday=1,
            start_time="10:00:00",
            end_time="15:00:00",
            location="Clinic B",
            is_active=True,
        )
        # Test retrieving the list of schedules
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_schedule(self):
        # Create a schedule to update
        schedule = Schedule.objects.create(
            doctor=self.doctor,
            weekday=2,
            start_time="08:00:00",
            end_time="14:00:00",
            location="Clinic C",
            is_active=True,
        )
        detail_url = reverse("schedule-detail", args=[schedule.id])
        updated_data = {
            "doctor": self.doctor.id,
            "weekday": 2,
            "start_time": "09:00:00",
            "end_time": "16:00:00",
            "location": "Clinic Updated",
            "is_active": False,
        }
        # Test updating the schedule
        response = self.client.put(detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schedule.refresh_from_db()
        self.assertEqual(schedule.location, "Clinic Updated")
        self.assertFalse(schedule.is_active)

    def test_delete_schedule(self):
        # Create a schedule to delete
        schedule = Schedule.objects.create(
            doctor=self.doctor,
            weekday=3,
            start_time="07:00:00",
            end_time="12:00:00",
            location="Clinic D",
            is_active=True,
        )
        detail_url = reverse("schedule-detail", args=[schedule.id])
        # Test deleting the schedule
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Schedule.objects.count(), 0)



@pytest.mark.django_db
class TestAppointmentSerializer:

    def setup_method(self):
        """Prepare shared test data: users and schedule"""
        self.patient = User.objects.create_user(username="patient", password="test123")
        self.doctor = User.objects.create_user(username="doctor", password="test123")
        self.schedule = Schedule.objects.create(doctor=self.doctor)

    def get_request(self, user):
        """Helper to create a fake POST request with user context"""
        factory = APIRequestFactory()
        request = factory.post("/appointments/", {})
        request.user = user
        return request

    def test_create_appointment_sets_created_by(self):
        """Ensure created_by is automatically set to request.user"""
        data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "schedule": self.schedule.id,
            "appointment_time": "09:00:00",
            "status": "Pending",
            "notes": "Initial consult",
        }

        request = self.get_request(self.patient)
        serializer = AppointmentSerializer(data=data, context={"request": request})

        assert serializer.is_valid(), serializer.errors
        appointment = serializer.save()

        assert appointment.created_by == self.patient
        assert appointment.doctor == self.doctor
        assert appointment.notes == "Initial consult"
        assert appointment.status == "Pending"

    def test_created_by_ignored_if_passed_in_data(self):
        """Even if created_by is passed, it should be ignored and overridden by request.user"""
        fake_user = User.objects.create_user(username="fake", password="12345")
        data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "schedule": self.schedule.id,
            "appointment_time": "10:00:00",
            "status": "Confirmed",
            "notes": "Follow-up",
            "created_by": fake_user.id  # This should be ignored
        }

        request = self.get_request(self.patient)
        serializer = AppointmentSerializer(data=data, context={"request": request})

        assert serializer.is_valid(), serializer.errors
        appointment = serializer.save()

        assert appointment.created_by == self.patient  # Not fake_user

    def test_invalid_status_fails_validation(self):
        """Serializer should fail if status is not a valid choice"""
        data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "schedule": self.schedule.id,
            "appointment_time": "11:00:00",
            "status": "InvalidStatus",  # Invalid
            "notes": "Bad status test",
        }

        request = self.get_request(self.patient)
        serializer = AppointmentSerializer(data=data, context={"request": request})

        assert not serializer.is_valid()
        assert "status" in serializer.errors

    def test_cancelled_status_sets_cancelled_at(self):
        """If status is set to 'Cancelled', cancelled_at should be set"""
        data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "schedule": self.schedule.id,
            "appointment_time": "12:00:00",
            "status": "Cancelled",
            "notes": "Canceled by patient",
        }

        request = self.get_request(self.patient)
        serializer = AppointmentSerializer(data=data, context={"request": request})
        assert serializer.is_valid(), serializer.errors
        appointment = serializer.save()

        # You need to make sure in your model/serializer you set cancelled_at if status == 'Cancelled'
        # Otherwise, this assertion will fail
        assert appointment.status == "Cancelled"
        assert appointment.cancelled_at is not None
        assert isinstance(appointment.cancelled_at, timezone.datetime.__class__) or isinstance(
            appointment.cancelled_at, timezone.datetime
        )
