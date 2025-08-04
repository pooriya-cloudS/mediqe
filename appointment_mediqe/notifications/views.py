from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AuditLog, Notification


# === Audit Logs ===


class AuditLogListView(LoginRequiredMixin, ListView):
    """
    View to list all audit logs for the logged-in user.
    Admins can filter logs for auditing purposes.
    """

    model = AuditLog
    template_name = "accounts/auditlog_list.html"
    context_object_name = "logs"

    def get_queryset(self):
        # Show only logs related to the current user unless the user is staff
        if self.request.user.is_staff:
            return AuditLog.objects.all().order_by("-timestamp")
        return AuditLog.objects.filter(user=self.request.user).order_by("-timestamp")


# === Notifications ===


class NotificationListView(LoginRequiredMixin, ListView):
    """
    View to list all notifications for the logged-in user.
    """

    model = Notification
    template_name = "accounts/notification_list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


class NotificationDetailView(LoginRequiredMixin, DetailView):
    """
    View to show a specific notification in detail.
    """

    model = Notification
    template_name = "accounts/notification_detail.html"
    context_object_name = "notification"

    def get_queryset(self):
        # Ensure user can only access their own notifications
        return Notification.objects.filter(user=self.request.user)


class MarkNotificationAsReadView(LoginRequiredMixin, View):
    """
    View to mark a notification as read and redirect back to notification list.
    """

    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return redirect("notification_list")  # name must match your URLconf
