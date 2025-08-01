from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from appointments.api.v1.serializers import AppointmentSerializer
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import time
from django.utils import timezone
from appointments.models import Appointment, Schedule
import pytest

User = get_user_model()


class AppointmentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        self.schedule = Schedule.objects.create(
            doctor=self.user,
            weekday=0,
            start_time=time(9, 0),
            end_time=time(12, 0),
            location="Clinic A",
            is_active=True,
        )
        self.appointment = Appointment.objects.create(
            doctor=self.user,
            patient=self.user,
            schedule=self.schedule,
            appointment_time=time(10, 0),
            status="Pending",
            created_by=self.user,
        )

    def test_create_appointment(self):
        url = reverse("appointment-create")
        data = {
            "doctor": self.user.id,
            "patient": self.user.id,
            "schedule": str(self.schedule.id),
            "appointment_time": "10:30:00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "Pending")

    def test_retrieve_appointment(self):
        url = reverse("appointment-detail", kwargs={"pk": self.appointment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.appointment.pk))

    def test_update_appointment_time(self):
        url = reverse("appointment-detail", kwargs={"pk": self.appointment.pk})
        response = self.client.patch(
            url, {"appointment_time": "11:00:00"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(str(self.appointment.appointment_time), "11:00:00")

    def test_delete_appointment(self):
        url = reverse("appointment-detail", kwargs={"pk": self.appointment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Appointment.objects.filter(pk=self.appointment.pk).exists())

    def test_cancel_appointment(self):
        url = reverse("appointment-cancel", kwargs={"pk": self.appointment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "Cancelled")
        self.assertIsNotNone(self.appointment.cancelled_at)

    def test_reschedule_appointment(self):
        url = reverse("appointment-reschedule", kwargs={"pk": self.appointment.pk})
        data = {"appointment_time": "11:30:00", "schedule": str(self.schedule.id)}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(str(self.appointment.appointment_time), "11:30:00")
        self.assertEqual(self.appointment.status, "Pending")

    def test_update_appointment_status(self):
        url = reverse("appointment-status-update", kwargs={"pk": self.appointment.pk})
        data = {"status": "Completed"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "Completed")


class ScheduleCRUDTestCase(APITestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username="doctor1", password="pass123")
        self.client.login(username="doctor1", password="pass123")
        self.list_url = reverse("schedule-list")
        self.schedule_data = {
            "doctor": self.doctor.id,
            "weekday": 0,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "location": "Clinic A",
            "is_active": True,
        }

    def test_create_schedule(self):
        response = self.client.post(self.list_url, self.schedule_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(Schedule.objects.get().location, "Clinic A")

    def test_read_schedule_list(self):
        Schedule.objects.create(
            doctor=self.doctor,
            weekday=1,
            start_time="10:00:00",
            end_time="15:00:00",
            location="Clinic B",
            is_active=True,
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_schedule(self):
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
        response = self.client.put(detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schedule.refresh_from_db()
        self.assertEqual(schedule.location, "Clinic Updated")
        self.assertFalse(schedule.is_active)

    def test_delete_schedule(self):
        schedule = Schedule.objects.create(
            doctor=self.doctor,
            weekday=3,
            start_time="07:00:00",
            end_time="12:00:00",
            location="Clinic D",
            is_active=True,
        )
        detail_url = reverse("schedule-detail", args=[schedule.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Schedule.objects.count(), 0)


@pytest.mark.django_db
class TestAppointmentSerializer:
    def setup_method(self):
        self.patient = User.objects.create_user(username="patient", password="test123")
        self.doctor = User.objects.create_user(username="doctor", password="test123")
        self.schedule = Schedule.objects.create(
            doctor=self.doctor,
            weekday=0,
            start_time=time(9, 0),
            end_time=time(12, 0),
            location="Clinic A",
            is_active=True,
        )

    def get_request(self, user):
        factory = APIRequestFactory()
        request = factory.post("/appointments/", {})
        request.user = user
        return request

    def test_create_appointment_sets_created_by(self):
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
        fake_user = User.objects.create_user(username="fake", password="12345")
        data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "schedule": self.schedule.id,
            "appointment_time": "10:00:00",
            "status": "Confirmed",
            "notes": "Follow-up",
            "created_by": fake_user.id,
        }
        request = self.get_request(self.patient)
        serializer = AppointmentSerializer(data=data, context={"request": request})
        assert serializer.is_valid(), serializer.errors
        appointment = serializer.save()
        assert appointment.created_by == self.patient

    def test_invalid_status_fails_validation(self):
        data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "schedule": self.schedule.id,
            "appointment_time": "11:00:00",
            "status": "InvalidStatus",
            "notes": "Bad status test",
        }
        request = self.get_request(self.patient)
        serializer = AppointmentSerializer(data=data, context={"request": request})
        assert not serializer.is_valid()
        assert "status" in serializer.errors

    def test_cancelled_status_sets_cancelled_at(self):
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
        assert appointment.status == "Cancelled"
        assert appointment.cancelled_at is not None
