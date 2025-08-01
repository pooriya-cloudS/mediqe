from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from appointment_mediqe.notifications.models import AuditLog, Notification

import uuid

User = get_user_model()


class AuditLogModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email='auditor@example.com',
            password='audit123',
            role='Admin',
            first_name='Audit',
            last_name='Logger',
            date_of_birth='1990-01-01',
            gender='Other',
            phone='0000000000',
            address='Log Street'
        )

        # Create an audit log entry
        self.log = AuditLog.objects.create(
            user=self.user,
            action="Login",
            target="Login System",
            ip_address="127.0.0.1",
            details="Successful login from Chrome browser"
        )

    def test_audit_log_created(self):
        # Check if the audit log entry exists and is linked correctly
        self.assertEqual(self.log.user, self.user)
        self.assertEqual(self.log.action, "Login")
        self.assertEqual(self.log.target, "Login System")
        self.assertEqual(self.log.ip_address, "127.0.0.1")
        self.assertIn("Chrome", self.log.details)

    def test_audit_log_str_method(self):
        # Check the string representation of the log
        self.assertIn(self.user.email, str(self.log))
        self.assertIn("Login", str(self.log))


class NotificationModelTest(TestCase):
    def setUp(self):
        # Create a user to receive notifications
        self.user = User.objects.create_user(
            email='notify@example.com',
            password='notify123',
            role='Patient',
            first_name='Notify',
            last_name='User',
            date_of_birth='2000-01-01',
            gender='Female',
            phone='9999999999',
            address='Notification Blvd'
        )

        # Create a notification
        self.notification = Notification.objects.create(
            user=self.user,
            type='APPOINTMENT',
            title='Appointment Reminder',
            content='You have an appointment with Dr. Smith tomorrow at 10 AM.'
        )

    def test_notification_created(self):
        # Validate the notification content
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.type, 'APPOINTMENT')
        self.assertFalse(self.notification.is_read)
        self.assertIn('Dr. Smith', self.notification.content)

    def test_notification_str_method(self):
        # Ensure string representation includes email and title
        self.assertIn(self.user.email, str(self.notification))
        self.assertIn('Appointment', str(self.notification))

