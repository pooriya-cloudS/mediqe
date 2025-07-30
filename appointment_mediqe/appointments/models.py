import uuid
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone


# Represents a doctor's working schedule
class Schedule(models.Model):
    # Primary key using UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link to the doctor (user)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="doctor_schedule",
    )

    # Weekday represented as an integer (0 = Monday, 6 = Sunday)
    weekday = models.IntegerField()

    # Start and end times for the schedule
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Location of the appointment or clinic
    location = models.CharField(max_length=100)

    # Whether this schedule is currently active
    is_active = models.BooleanField(default=False)


# Represents a patient appointment
class Appointment(models.Model):
    # Primary key using UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Possible status values for an appointment
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
        ("NoShow", "NoShow"),
    ]

    # Link to the doctor
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="doctor_appointment",
    )

    # Link to the patient (standard Django User)
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patient_appointment",
        blank=True,
        null=True,
    )

    # Link to the schedule this appointment belongs to
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, blank=True, null=True
    )

    # The time of the actual appointment
    appointment_time = models.TimeField()

    # Current status of the appointment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    # User who created the appointment
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Timestamp of when the appointment was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp of when the appointment was cancelled (if applicable)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    # Optional notes about the appointment
    notes = models.TextField(blank=True)

    # Override save method to auto-set or clear the cancellation time
    def save(self, *args, **kwargs):
        if self.status == "Cancelled" and not self.cancelled_at:
            self.cancelled_at = timezone.now()
        elif self.status != "Cancelled":
            self.cancelled_at = None
        super().save(*args, **kwargs)
