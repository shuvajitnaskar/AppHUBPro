from django.db import models
from django.contrib.auth.models import User

# ১. ইউজার প্রোফাইল মডেল
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    github = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

# ২. মেইন অ্যাপ/কন্টেন্ট আপলোড মডেল
class UploadedContent(models.Model):
    CONTENT_TYPES = (
        ('app', 'Application'),
        ('photo', 'Photo'),
        ('video', 'Video'),
    )

    title = models.CharField(max_length=200)
    # এখানে default দেওয়া হয়েছে যাতে মাইগ্রেশনে এরর না আসে
    description = models.TextField(default="No description provided")
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='app')
    file = models.FileField(upload_to='uploads/')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    downloads = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# ৩. অ্যাপ ভার্সন হিস্ট্রি মডেল
class AppVersion(models.Model):
    app = models.ForeignKey(UploadedContent, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50) 
    changelog = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/versions/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.app.title} - {self.version_number}"

# ৪. অ্যাপ রিকোয়েস্ট মডেল
class AppRequest(models.Model):
    # এখানেও null=True দেওয়া হয়েছে পুরনো ডেটা হ্যান্ডেল করার জন্য
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    app_name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.app_name

class Content(models.Model):
    file_url = models.URLField(max_length=500, blank=True, null=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)