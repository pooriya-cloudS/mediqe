import os
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from ...models import MedicalFile, MedicalRecord
from .serializers import MedicalFileSerializer


@extend_schema(
    request=MedicalFileSerializer,
    responses={
        201: MedicalFileSerializer,
        400: OpenApiResponse(description="Invalid input"),
        403: OpenApiResponse(description="Permission denied"),
    },
    summary="Upload a medical file",
    description="""
    Upload a file to a specific medical record.

    **Permissions**: Only the patient or doctor associated with the medical record can upload files.

    Fields:
    - `record`: UUID of the medical record
    - `file`: File to upload (multipart/form-data)
    - `type`: Type of file (e.g., "MRI", "Lab Report")
    - `description`: Optional description
    - `is_private`: Boolean, whether this file is restricted
    """,
    tags=["Medical Files"],
)
class MedicalFileUploadView(generics.CreateAPIView):
    # Serializer to handle MedicalFile data validation and creation
    serializer_class = MedicalFileSerializer

    # Only authenticated users can upload files
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Extract the medical record ID from request data
        record_id = self.request.data.get("record")

        # Retrieve the corresponding medical record or return 404 if not found
        record = get_object_or_404(MedicalRecord, id=record_id)

        # Permission check: allow upload only if user is patient or doctor of this record
        if self.request.user != record.patient and self.request.user != record.doctor:
            raise PermissionDenied("You do not have permission to upload files.")

        # Save the uploaded file instance and assign current user as uploader
        serializer.save(uploader=self.request.user)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="pk",
            location=OpenApiParameter.PATH,
            required=True,
            description="UUID of the medical file to download",
            type=str,
        ),
    ],
    responses={
        200: OpenApiResponse(description="Returns the file as attachment"),
        403: OpenApiResponse(description="Permission denied"),
        404: OpenApiResponse(description="File not found"),
    },
    summary="Download a medical file",
    description="""
    Download a medical file (PDF, Image, etc.) if you are the patient, the doctor, or the person who uploaded the file.

    **Returns**: Binary file content as attachment.
    """,
    tags=["Medical Files"],
)
class MedicalFileDownloadView(generics.GenericAPIView):
    # Only authenticated users can download files
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        # Retrieve the medical file object or 404 if it doesn't exist
        medical_file = get_object_or_404(MedicalFile, id=pk)
        record = medical_file.record
        user = request.user

        # Permission check: user must be patient, doctor, or uploader to access the file
        if (
            user != record.patient
            and user != record.doctor
            and user != medical_file.uploader
        ):
            raise PermissionDenied("You do not have permission to access this file.")

        try:
            # Attempt to open the file from the stored file_path and return it as a response attachment
            return FileResponse(
                open(medical_file.file_path, "rb"),
                as_attachment=True,
                filename=os.path.basename(medical_file.file_path),
            )
        except FileNotFoundError:
            # Raise 404 error if the file does not exist on disk
            raise Http404("File not found.")
