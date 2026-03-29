from django.db import models
from django.contrib.auth.models import User

class UploadedContent(models.Model):
    CONTENT_CHOICES = [
        ('app', 'App'),
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_CHOICES)
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)
    total_votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.content_type}"