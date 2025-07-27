import uuid
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


# MedicalRecord model to store patient medical history and visit details
class MedicalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier for each medical record

    STATUS_CHOICES = [
        ('Open', 'Open'),       # Record is currently active/open
        ('Closed', 'Closed'),   # Record is closed, no new entries expected
        ('Archived', 'Archived'), # Record archived for long-term storage
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='patient_record'
    )  # Reference to the patient user
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='doctor_record'
    )  # Reference to the doctor responsible for the record

    visit_reason = models.TextField(blank=True, null=True)  # Reason for patient's visit
    diagnosis = models.TextField(blank=True, null=True)     # Diagnosis details
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')  # Current status of the record
    is_sensitive = models.BooleanField(default=False)       # Indicates if the record contains sensitive information
    created_at = models.DateTimeField(auto_now_add=True)    # Timestamp when record was created
    updated_at = models.DateTimeField(auto_now=True)        # Timestamp when record was last updated


# Prescription model to store medication prescribed in a medical record
class Prescription(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),         # Prescription is currently active
        ('Completed', 'Completed'),   # Prescription course completed
        ('Cancelled', 'Cancelled'),   # Prescription cancelled
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier for each prescription
    record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )  # Link to the related medical record

    medication = models.CharField(max_length=100)    # Name of the medication prescribed
    dosage = models.CharField(max_length=100)        # Dosage instructions (e.g., "2 tablets daily")
    instructions = models.TextField()                 # Additional instructions for taking the medication
    start_date = models.DateField()                    # Prescription start date
    end_date = models.DateField()                      # Prescription end date
    renewable = models.BooleanField(default=False)    # Whether the prescription can be renewed
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')  # Current status of the prescription


# MedicalFile model to store files related to a medical record (e.g., scans, reports)
class MedicalFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier for each file
    record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='files'
    )  # Link to the related medical record

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User who uploaded the file
    file_path = models.CharField(max_length=200)                  # Path or URL to the file
    type = models.CharField(max_length=50)                        # Type of the file (e.g., "X-Ray", "Lab Report")
    size = models.IntegerField()                                  # File size in bytes
    description = models.TextField()                              # Description or notes about the file
    uploaded_at = models.DateTimeField(auto_now_add=True)        # Timestamp when the file was uploaded
    is_private = models.BooleanField(default=False)              # Whether the file is private (restricted access)
