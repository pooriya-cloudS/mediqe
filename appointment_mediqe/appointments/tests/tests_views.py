from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from ..models import Schedule
import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from appointments.api.v1.serializers import AppointmentSerializer

User = get_user_model()

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
