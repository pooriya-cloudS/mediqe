
# accounts/models.py
import uuid
from django.db import models
from django.conf import settings


# === Audit Log Model ===
class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    # Unique identifier for each log entry

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='audit_logs')
    # The user who performed the action

    action = models.CharField(max_length=255)
    # The action performed (e.g., "Login", "Update Profile", "Delete Appointment")

    target = models.CharField(max_length=255)
    # The object or resource affected by the action (e.g., "UserProfile", "Appointment #123")

    timestamp = models.DateTimeField(auto_now_add=True)
    # When the action occurred

    ip_address = models.GenericIPAddressField()
    # IP address of the user or client making the request

    details = models.TextField()
    # Optional detailed description or metadata (e.g., JSON, plain text)

    def __str__(self):
        return f"{self.user.email} - {self.action} @ {self.timestamp}"


# === Notification Model ===
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('APPOINTMENT', 'Appointment'),
        ('MESSAGE', 'Message'),
        ('PAYMENT', 'Payment'),
        ('SYSTEM', 'System'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Unique ID for the notification

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    # The recipient user of the notification

    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    # Notification type/category

    title = models.CharField(max_length=255)
    # Short title (e.g., "New Message from Doctor")

    content = models.TextField()
    # Detailed content/message body

    is_read = models.BooleanField(default=False)
    # True if the user has read this notification

    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the notification was created

    def __str__(self):
        return f"{self.user.email} - {self.type} - {self.title}"

