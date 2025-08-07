from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from ...models import MedicalFile, MedicalRecord
from .serializers import MedicalFileSerializer
from django.http import FileResponse, Http404


class MedicalFileUploadView(generics.CreateAPIView):
    serializer_class = MedicalFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get the medical record ID from the request data
        record_id = self.request.data.get("record")
        # Retrieve the medical record or return 404 if not found
        record = get_object_or_404(MedicalRecord, id=record_id)

        # Allow upload only if the user is the patient or the doctor of the record
        if self.request.user != record.patient and self.request.user != record.doctor:
            raise PermissionDenied("You do not have permission to upload files.")

        # Save the uploaded file with the current user as uploader
        serializer.save(uploader=self.request.user)


class MedicalFileDownloadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        # Retrieve the medical file or return 404 if not found
        medical_file = get_object_or_404(MedicalFile, id=pk)
        record = medical_file.record
        user = request.user

        # Allow download only if the user is patient, doctor, or uploader of the file
        if (
            user != record.patient
            and user != record.doctor
            and user != medical_file.uploader
        ):
            raise PermissionDenied("You do not have permission to access this file.")

        # Return the file as an attachment in the response
        return FileResponse(
            medical_file.file.open(),
            as_attachment=True,
            filename=medical_file.file.name,
        )
