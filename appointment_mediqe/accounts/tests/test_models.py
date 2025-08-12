import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appointment_mediqe.settings")
django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()


class UserModelTest(TestCase):

    def create_user(self, **kwargs):
        return User.objects.create_user(
            email=kwargs.get("email", "test@example.com"),
            password=kwargs.get("password", "password123"),
            username=kwargs.get("username", "testuser"),
            role=kwargs.get("role", "Patient"),
            first_name=kwargs.get("first_name", "Test"),
            last_name=kwargs.get("last_name", "User"),
            gender=kwargs.get("gender", "Male"),
            phone=kwargs.get("phone", "1234567890"),
            address=kwargs.get("address", "Test Address"),
        )

    def test_create_user(self):
        user = self.create_user()
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(user.role, "Patient")

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertEqual(superuser.email, "admin@example.com")


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="profiletest@example.com",
            password="password123",
            username="profileuser",
            role="Doctor",
            first_name="Test",
            last_name="Doctor",
            gender="Female",
            phone="0987654321",
            address="Sample Address",
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            insurance_number="INS123456",
            insurance_company="HealthInsure",
            blood_type="A+",
            chronic_conditions="Diabetes",
            license_number="LIC123456",
            specialty="Cardiology",
            bio="Experienced cardiologist.",
            years_experience=10,
            rating=4.5,
            verified=True,
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.email, "profiletest@example.com")
        self.assertEqual(self.profile.blood_type, "A+")
        self.assertEqual(self.profile.years_experience, 10)
        self.assertEqual(self.profile.rating, 4.5)
        self.assertTrue(self.profile.verified)
