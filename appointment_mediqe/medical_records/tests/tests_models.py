from django.test import TestCase
from django.contrib.auth.models import User
from ..models import MedicalRecord, Prescription, MedicalFile
from datetime import date
import uuid


class MedicalRecordTest(TestCase):
    def test_create_medical_record(self):
        # Create a MedicalRecord instance with test data
        record = MedicalRecord.objects.create(
            visit_reason="Headache and dizziness",  # Reason for visit
            diagnosis="Migraine",                    # Diagnosis given
            status="Open",                           # Status of the medical record
            is_sensitive=True                        # Mark the record as sensitive
        )
        # Assert the record ID is a valid UUID
        self.assertIsInstance(record.id, uuid.UUID)
        # Assert the status is correctly set
        self.assertEqual(record.status, "Open")
        # Assert the sensitive flag is True
        self.assertTrue(record.is_sensitive)
        # Assert the visit reason is correctly set
        self.assertEqual(record.visit_reason, "Headache and dizziness")


class PrescriptionTest(TestCase):
    def setUp(self):
        # Create a MedicalRecord to link prescriptions to
        self.record = MedicalRecord.objects.create(
            diagnosis="Hypertension",  # Diagnosis for the record
            status="Open",
        )

    def test_create_prescription(self):
        # Create a Prescription linked to the MedicalRecord
        prescription = Prescription.objects.create(
            record=self.record,                      # Link to medical record
            medication="Losartan",                   # Medication name
            dosage="50mg",                          # Dosage information
            instructions="Take once daily after breakfast",  # Usage instructions
            start_date=date.today(),                 # Start date of prescription
            end_date=date.today(),                   # End date of prescription
            renewable=True,                         # Can this prescription be renewed?
            status="Active"                         # Current status of prescription
        )
        # Assert medication name is correct
        self.assertEqual(prescription.medication, "Losartan")
        # Assert prescription is linked to the correct medical record diagnosis
        self.assertEqual(prescription.record.diagnosis, "Hypertension")
        # Assert renewable flag is True
        self.assertTrue(prescription.renewable)


class MedicalFileTest(TestCase):
    def setUp(self):
        # Create a user who will upload medical files
        self.user = User.objects.create_user(username="uploader1", password="123456")
        # Create a MedicalRecord to associate files with
        self.record = MedicalRecord.objects.create(diagnosis="Diabetes", status="Open")

    def test_create_medical_file(self):
        # Create a MedicalFile linked to a MedicalRecord and uploaded by a user
        file = MedicalFile.objects.create(
            record=self.record,                       # Link to medical record
            uploader=self.user,                       # User who uploaded the file
            file_path="/media/files/report123.pdf", # Path or URL of the file
            type="PDF",                              # File type
            size=2048,                              # File size in bytes
            description="Blood sugar report",       # Description of the file
            is_private=True                         # Whether the file is private
        )

        # Assert file type is correct
        self.assertEqual(file.type, "PDF")
        # Assert file size is correct
        self.assertEqual(file.size, 2048)
        # Assert is_private flag is True
        self.assertTrue(file.is_private)
        # Assert uploader's username is correct
        self.assertEqual(file.uploader.username, "uploader1")
