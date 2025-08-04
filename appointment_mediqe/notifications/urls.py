from django.urls import path
from .views import (
    AuditLogListView,
    NotificationListView,
    NotificationDetailView,
    MarkNotificationAsReadView,
)

urlpatterns = [
    path("audit-logs/", AuditLogListView.as_view(), name="auditlog_list"),
    path("notifications/", NotificationListView.as_view(), name="notification_list"),
    path(
        "notifications/<uuid:pk>/",
        NotificationDetailView.as_view(),
        name="notification_detail",
    ),
    path(
        "notifications/<uuid:pk>/read/",
        MarkNotificationAsReadView.as_view(),
        name="notification_mark_read",
    ),
]
