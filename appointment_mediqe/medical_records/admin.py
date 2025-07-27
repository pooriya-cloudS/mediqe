from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(MedicalRecord)
admin.site.register(MedicalFile)
admin.site.register(Prescription)
