from rest_framework import serializers
from .models import UploadedFile

# Serializes the UploadedFile model, allowing the file upload and representation of the uploaded file's metadata
class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at']
