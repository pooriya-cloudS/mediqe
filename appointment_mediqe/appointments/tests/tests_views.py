from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from ..models import Schedule


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
