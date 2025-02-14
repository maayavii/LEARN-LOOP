# models.py
from django.db import models

class FileConversion(models.Model):
    input_file = models.FileField(upload_to='uploads/')
    output_file = models.FileField(upload_to='converted/', null=True)
    input_format = models.CharField(max_length=10)
    output_format = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    error_message = models.TextField(blank=True, null=True)

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=10)  # pdf, docx, pptx
    uploaded_at = models.DateTimeField(auto_now_add=True)
    edited_file = models.FileField(upload_to='edited/', null=True, blank=True)

    def __str__(self):
        return f"{self.file.name} ({self.file_type})"