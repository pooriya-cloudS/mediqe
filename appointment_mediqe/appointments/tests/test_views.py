from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.models import User
from ..models import Appointment, Schedule


class AppointmentViewSetTestCase(TestCase):
    def setUp(self):
        # Create doctor and patient users
        self.doctor = User.objects.create_user(username="doctor", password="pass123")
        self.patient = User.objects.create_user(username="patient", password="pass123")

        # Authenticate API client as patient
        self.client = APIClient()
        self.client.force_authenticate(user=self.patient)

        # Create schedule for doctor
        self.schedule = Schedule.objects.create(
            id=uuid4(),
            doctor=self.doctor,
            weekday=1,
            start_time="09:00",
            end_time="17:00",
            location="Clinic A",
            is_active=True,
        )

        # Create an appointment
        self.appointment = Appointment.objects.create(
            id=uuid4(),
            doctor=self.doctor,
            patient=self.patient,
            schedule=self.schedule,
            appointment_time=timezone.now().time(),
            status="Pending",
            created_by=self.patient,
        )

    def test_cancel_appointment(self):
        url = reverse("appointments-cancel", args=[self.appointment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "Cancelled")
        self.assertIsNotNone(self.appointment.cancelled_at)

    def test_cancel_already_cancelled_appointment(self):
        self.appointment.status = "Cancelled"
        self.appointment.save()

        url = reverse("appointments-cancel", args=[self.appointment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already cancelled", response.data["detail"].lower())

    def test_reschedule_appointment(self):
        url = reverse("appointments-reschedule", args=[self.appointment.id])
        new_time = timezone.now().time()
        data = {
            "appointment_time": new_time.isoformat(),
            "schedule": str(self.schedule.id),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "Pending")
        self.assertEqual(
            self.appointment.appointment_time.isoformat(), new_time.isoformat()
        )

    def test_reschedule_missing_fields(self):
        url = reverse("appointments-reschedule", args=[self.appointment.id])
        data = {"appointment_time": timezone.now().time().isoformat()}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("schedule", response.data)

    def test_update_status(self):
        url = reverse("appointments-update-status", args=[self.appointment.id])
        response = self.client.post(url, {"status": "Confirmed"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "Confirmed")

    def test_update_status_missing(self):
        url = reverse("appointments-update-status", args=[self.appointment.id])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
