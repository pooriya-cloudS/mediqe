from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import MedicalRecord, MedicalFile
from django.contrib.auth import get_user_model

User = get_user_model()

class MedicalFileTests(TestCase):
    def setUp(self):
        # Create users: patient, doctor, and an unrelated user
        self.patient = User.objects.create_user(username='patient', password='pass')
        self.doctor = User.objects.create_user(username='doctor', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')

        # Create a medical record linked to patient and doctor
        self.record = MedicalRecord.objects.create(patient=self.patient, doctor=self.doctor)

        # Initialize DRF API client
        self.client = APIClient()

    def test_upload_medical_file_success(self):
        # Authenticate as patient (allowed user)
        self.client.force_authenticate(user=self.patient)

        # Prepare a simple PDF file for upload
        file_data = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")

        # Prepare POST data including the medical record ID
        url = reverse('medicalfile-upload')
        data = {
            "record": str(self.record.id),
            "file": file_data,
            "type": "Lab Report",
            "description": "Test file"
        }

        # Perform POST request to upload the file
        response = self.client.post(url, data, format='multipart')

        # Assert the upload was successful (HTTP 201 Created)
        self.assertEqual(response.status_code, 201)
        # Check that the MedicalFile object was created in the database
        self.assertTrue(MedicalFile.objects.filter(record=self.record).exists())
        # Verify the response contains the correct file type
        self.assertEqual(response.data['type'], "Lab Report")

    def test_upload_medical_file_permission_denied(self):
        # Authenticate as an unauthorized user
        self.client.force_authenticate(user=self.other_user)

        # Prepare a simple PDF file for upload
        file_data = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")

        url = reverse('medicalfile-upload')
        data = {
            "record": str(self.record.id),
            "file": file_data,
            "type": "Lab Report",
            "description": "Test file"
        }

        # Attempt to upload the file, expecting permission denied
        response = self.client.post(url, data, format='multipart')

        # Assert that the response status is 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_download_medical_file_success(self):
        # Create a MedicalFile instance associated with the record and patient
        medical_file = MedicalFile.objects.create(
            record=self.record,
            uploader=self.patient,
            file=SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf"),
            type="Lab Report",
            description="desc"
        )

        # Authenticate as patient (allowed to download)
        self.client.force_authenticate(user=self.patient)

        url = reverse('medicalfile-download', args=[medical_file.id])
        response = self.client.get(url)

        # Assert the download was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the file as an attachment
        self.assertIn('attachment', response.get('Content-Disposition', ''))
        # Verify the content type of the returned file
        self.assertEqual(response.get('Content-Type'), 'application/pdf')

    def test_download_medical_file_permission_denied(self):
        # Create a MedicalFile instance
        medical_file = MedicalFile.objects.create(
            record=self.record,
            uploader=self.patient,
            file=SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf"),
            type="Lab Report",
            description="desc"
        )

        # Authenticate as an unauthorized user
        self.client.force_authenticate(user=self.other_user)

        url = reverse('medicalfile-download', args=[medical_file.id])
        response = self.client.get(url)

        # Assert the download is forbidden for unauthorized users
        self.assertEqual(response.status_code, 403)
