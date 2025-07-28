from django.test import TestCase
from django.test import TestCase
from accounts.models import User
import uuid
from datetime import date

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=uuid.uuid4(),
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            role="Patient",
            first_name="Ali",
            last_name="Ahmadi",
            date_of_birth=date(1990, 1, 1),
            gender="Male",
            phone="09123456789",
            address="Tehran, Iran",
        )

    def test_user_created_successfully(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_verified)

    def test_str_representation(self):
        self.assertEqual(str(self.user), "testuser")

    def test_email_is_unique(self):
        with self.assertRaises(Exception):
            User.objects.create(
                id=uuid.uuid4(),
                username="anotheruser",
                email="test@example.com",  # تکراری
                password="anotherpassword",
                role="Doctor",
                first_name="Reza",
                last_name="Karimi",
                date_of_birth=date(1985, 5, 5),
                gender="Male",
                phone="09351234567",
                address="Mashhad",
            )

from django.test import TestCase
from accounts.models import User, UserProfile
import uuid
from datetime import date

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=uuid.uuid4(),
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            role="Doctor",
            first_name="Ali",
            last_name="Ahmadi",
            date_of_birth=date(1985, 5, 10),
            gender="Male",
            phone="09123456789",
            address="Tehran",
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            insurance_number="123456789",
            insurance_company="Tehran Insurance",
            blood_type="A+",
            chronic_conditions="Diabetes",
            license_number="LIC12345",
            specialty="Cardiology",
            bio="Experienced heart specialist.",
            years_experience=10,
            rating=4.8,
            verified=True
        )

    def test_userprofile_created_successfully(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.insurance_company, "Tehran Insurance")
        self.assertEqual(self.profile.blood_type, "A+")
        self.assertTrue(self.profile.verified)
        self.assertAlmostEqual(self.profile.rating, 4.8)

    def test_str_representation(self):
        self.assertEqual(str(self.profile), "testuser Profile")

from django.test import TestCase
from accounts.models import User, AuditLog, Notification
import uuid
from datetime import date

class AuditLogModelTest(TestCase):
    def setUp(self):
        # اول یک یوزر بساز
        self.user = User.objects.create(
            id=uuid.uuid4(),
            username="logger",
            email="logger@example.com",
            password="pass1234",
            role="Admin",
            first_name="Log",
            last_name="Ger",
            date_of_birth=date(1980, 1, 1),
            gender="Other",
            phone="09120000000",
            address="Somewhere",
        )
        # بعد یک رکورد لاگ
        self.log = AuditLog.objects.create(
            id=uuid.uuid4(),
            user=self.user,
            action="CREATE",
            target="UserProfile",
            ip_address="192.168.1.1",
            details="Created profile for user",
        )

    def test_auditlog_created(self):
        self.assertEqual(self.log.user, self.user)
        self.assertEqual(self.log.action, "CREATE")
        self.assertEqual(self.log.target, "UserProfile")
        self.assertEqual(self.log.ip_address, "192.168.1.1")
        self.assertEqual(self.log.details, "Created profile for user")
        # timestamp خودکار ست شده
        self.assertIsNotNone(self.log.timestamp)

    def test_str_representation(self):
        self.assertEqual(str(self.log), "CREATE by logger")


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=uuid.uuid4(),
            username="notify",
            email="notify@example.com",
            password="pass5678",
            role="Patient",
            first_name="No",
            last_name="Tify",
            date_of_birth=date(1995, 2, 2),
            gender="Female",
            phone="09330000000",
            address="Elsewhere",
        )
        self.notif = Notification.objects.create(
            id=uuid.uuid4(),
            user=self.user,
            type="Info",
            title="Welcome",
            content="Welcome to our service!",
        )

    def test_notification_created(self):
        self.assertEqual(self.notif.user, self.user)
        self.assertEqual(self.notif.type, "Info")
        self.assertEqual(self.notif.title, "Welcome")
        self.assertEqual(self.notif.content, "Welcome to our service!")
        # مقدار پیش‌فرض
        self.assertFalse(self.notif.is_read)
        self.assertIsNotNone(self.notif.created_at)

    def test_str_representation(self):
        self.assertEqual(str(self.notif), "Welcome → notify")
