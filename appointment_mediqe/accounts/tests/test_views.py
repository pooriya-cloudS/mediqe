import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appointment_mediqe.settings")
django.setup()

from django.test import TestCase
from accounts.models import User, UserProfile
from django.utils import timezone
import uuid


class UserModelTest(TestCase):
    def test_create_regular_user(self):
        """Test creating a regular user with email and password"""
        user = User.objects.create_user(
            email="userr@example.com",
            password="testpassword123",
            role="Patient",
            first_name="John",
            last_name="Doe",
            gender="Male",
            phone="1234567890",
            address="123 Street",
        )

        self.assertEqual(user.email, "userr@example.com")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertEqual(user.role, "Patient")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            email="adminn@example.com", password="adminpassword"
        )

        self.assertEqual(admin.email, "adminn@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password("adminpassword"))

    def test_user_str_method(self):
        """Test string representation of User"""
        user = User.objects.create_user(email="strr@example.com", password="123456")
        self.assertEqual(str(user), "strr@example.com (Patient)")

    def test_user_extra_info_json_field(self):
        """Test setting and retrieving extra_info JSON field"""
        data = {"height": 180, "weight": 70}
        user = User.objects.create_user(
            email="jsonn@example.com", password="123456", extra_info=data
        )
        self.assertEqual(user.extra_info["height"], 180)
        self.assertEqual(user.extra_info["weight"], 70)


class UserProfileModelTest(TestCase):
    def setUp(self):
        """Create a user for linking to profile"""
        self.user = User.objects.create_user(
            email="profileuserr@example.com",
            password="testpass",
            role="Doctor",
            first_name="Alice",
            last_name="Smith",
            gender="Female",
            phone="111222333",
            address="456 Street",
        )

    def test_create_user_profile(self):
        """Test creating a user profile and linking it to user"""
        profile = UserProfile.objects.create(
            user=self.user,
            insurance_number="INS12345",
            insurance_company="HealthPlus",
            blood_type="O+",
            chronic_conditions="Hypertension",
            license_number="DOC98765",
            specialty="Cardiology",
            bio="Experienced heart doctor",
            years_experience=10,
            rating=4.7,
            verified=True,
        )

        self.assertEqual(profile.user.email, "profileuserr@example.com")
        self.assertEqual(profile.specialty, "Cardiology")
        self.assertEqual(profile.blood_type, "O+")
        self.assertTrue(profile.verified)

    def test_profile_str_method(self):
        """Test string representation of profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            insurance_number="INS123",
            insurance_company="CareX",
            blood_type="A+",
            chronic_conditions="None",
            license_number="DOC00001",
            specialty="General",
            bio="Just a doctor",
            years_experience=3,
            rating=4.2,
            verified=False,
        )
        self.assertEqual(str(profile), "profileuserr@example.com Profile")
