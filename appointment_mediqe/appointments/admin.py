from django.contrib import admin

from appointments.models import Schedule, Appointment

# Register your models here.
admin.site.register(Schedule)
admin.site.register(Appointment)
