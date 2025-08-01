from django.test import TestCase
from models import User
from uuid import uuid4
from datetime import date

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=uuid4(),
            username='testuser',
            email='test@example.com',
            password='pass1234',
            role='Patient',
            first_name='Test',
            last_name='User',
            date_of_birth=date(1990, 1, 1),
            gender='Male',
            phone='09123456789',
            address='Test Address',
        )

    def test_user_created(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.is_active)

    def test_str_representation(self):
        self.assertEqual(str(self.user), 'test@example.com')
        
# accounts/tests/test_userprofile.py
from django.test import TestCase
from accounts.models import User, UserProfile
from datetime import date

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="securepassword123",
            username="testuser",
            role="Doctor",
            first_name="Ali",
            last_name="Ahmadi",
            date_of_birth=date(1990, 5, 15),
            gender="Male",
            phone="09123456789",
            address="Tehran"
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            insurance_number="INS123456",
            insurance_company="Tamin",
            blood_type="A+",
            chronic_conditions="Asthma",
            license_number="DOC456",
            specialty="Dermatology",
            bio="Experienced skin specialist",
            years_experience=8,
            rating=4.7,
            verified=True
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.email, "test@example.com")
        self.assertEqual(self.profile.blood_type, "A+")
        self.assertTrue(self.profile.verified)
        self.assertEqual(self.profile.years_experience, 8)

    def test_str_representation(self):
        self.assertEqual(str(self.profile), "test@example.com Profile")
#test