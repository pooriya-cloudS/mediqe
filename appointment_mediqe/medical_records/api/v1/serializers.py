from rest_framework import serializers
from ...models import MedicalFile

ALLOWED_EXTENSIONS = ["pdf", "jpg", "jpeg", "png"]


class MedicalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFile
        fields = [
            "id",
            "record",
            "uploader",
            "file",
            "type",
            "description",
            "uploaded_at",
            "is_private",
        ]
        read_only_fields = ["id", "uploader", "uploaded_at"]

    def validate_file(self, value):
        ext = value.name.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                "فرمت فایل باید PDF، JPG، JPEG یا PNG باشد."
            )
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("حجم فایل باید کمتر از ۵ مگابایت باشد.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["uploader"] = request.user
        return super().create(validated_data)
