import uuid
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class MedicalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Archived', 'Archived'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True,related_name='patient_record')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='doctor_record',blank=True, null=True)
    visit_reason = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    is_sensitive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Prescription(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    renewable = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')


class MedicalFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='files')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    size = models.IntegerField()
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)