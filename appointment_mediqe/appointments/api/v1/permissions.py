from rest_framework.permissions import BasePermission


class AccessViewAppointment(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff:
            return True
        if hasattr(user, "role") and user.role == "doctor":
            return obj.doctor == user

        return obj.patient == user


class AccessViewSchedule(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True
        return None
