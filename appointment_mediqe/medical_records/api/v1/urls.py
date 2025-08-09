from django.urls import path
from .views import *

urlpatterns = [
    path(
        "records/<uuid:record_id>/upload/",
        MedicalFileUploadView.as_view(),
        name="upload_medical_file",
    ),
    path(
        "files/<uuid:file_id>/download/",
        MedicalFileDownloadView.as_view(),
        name="download_medical_file",
    ),
]
