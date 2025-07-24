from django.test import TestCase
from django.contrib.auth.models import User
from .models import MedicalRecord, Prescription, MedicalFile
from datetime import date
import uuid

class MedicalRecordTest(TestCase):
    def test_create_medical_record(self):
        record = MedicalRecord.objects.create(
            visit_reason="Headache and dizziness",
            diagnosis="Migraine",
            status="Open",
            is_sensitive=True
        )
        self.assertIsInstance(record.id, uuid.UUID)
        self.assertEqual(record.status, "Open")
        self.assertTrue(record.is_sensitive)
        self.assertEqual(record.visit_reason, "Headache and dizziness")

class PrescriptionTest(TestCase):
    def setUp(self):
        self.record = MedicalRecord.objects.create(
            diagnosis="Hypertension",
            status="Open",
        )

    def test_create_prescription(self):
        prescription = Prescription.objects.create(
            record=self.record,
            medication="Losartan",
            dosage="50mg",
            instructions="Take once daily after breakfast",
            start_date=date.today(),
            end_date=date.today(),
            renewable=True,
            status="Active"
        )
        self.assertEqual(prescription.medication, "Losartan")
        self.assertEqual(prescription.record.diagnosis, "Hypertension")
        self.assertTrue(prescription.renewable)

class MedicalFileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="uploader1", password="123456")
        self.record = MedicalRecord.objects.create(diagnosis="Diabetes", status="Open")

    def test_create_medical_file(self):
        file = MedicalFile.objects.create(
            record=self.record,
            uploader=self.user,
            file_path="/media/files/report123.pdf",
            type="PDF",
            size=2048,
            description="Blood sugar report",
            is_private=True
        )
        self.assertEqual(file.type, "PDF")
        self.assertEqual(file.size, 2048)
        self.assertTrue(file.is_private)
        self.assertEqual(file.uploader.username, "uploader1")