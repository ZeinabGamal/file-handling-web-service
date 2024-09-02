from django.db import models


# model representing an uploaded file.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploaded_files/')
    # A timestamp that records when the file was uploaded.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
