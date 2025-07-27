import uuid
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


# Schedule model to represent a doctor's working hours on a particular day
class Schedule(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # Unique identifier for each schedule
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="doctor_schedule",
    )  # Reference to the doctor user
    weekday = models.IntegerField()  # Day of the week (e.g., 0=Monday, 6=Sunday)
    start_time = models.TimeField()  # Schedule start time
    end_time = models.TimeField()  # Schedule end time
    location = models.CharField(max_length=100)  # Location of the appointment
    is_active = models.BooleanField(
        default=False
    )  # Indicates if the schedule is currently active


# Appointment model to represent a patient's appointment with a doctor
class Appointment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # Unique identifier for each appointment

    STATUS_CHOICES = [
        ("Pending", "Pending"),  # Appointment requested, awaiting confirmation
        ("Confirmed", "Confirmed"),  # Appointment confirmed by doctor or patient
        ("Cancelled", "Cancelled"),  # Appointment cancelled
        ("Completed", "Completed"),  # Appointment completed
        ("NoShow", "NoShow"),  # Patient did not show up
    ]

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="doctor_appointment",
    )  # Reference to the doctor user
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patient_appointment",
        blank=True,
        null=True,
    )  # Reference to the patient user
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, blank=True, null=True
    )  # Reference to the schedule associated with this appointment
    appointment_time = models.TimeField()  # Time of the appointment
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending"
    )  # Current status of the appointment
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # User who created the appointment (could be doctor or admin)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the appointment was created
    cancelled_at = models.DateTimeField(
        blank=True, null=True
    )  # Timestamp when the appointment was last updated (e.g., cancellation)
    notes = models.TextField(blank=True)  # Optional notes related to the appointment
