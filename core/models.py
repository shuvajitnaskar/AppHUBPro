from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ---------------------------------------------------
# ১. ইউজার প্রোফাইল মডেল (সোশ্যাল লিঙ্ক ও বায়ো সহ)
# ---------------------------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True, default="Premium App Developer at AppHUBPro")
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # সোশ্যাল মিডিয়া লিঙ্কসমূহ
    instagram = models.URLField(max_length=255, blank=True, null=True, placeholder="https://instagram.com/yourprofile")
    facebook = models.URLField(max_length=255, blank=True, null=True)
    sharechat = models.URLField(max_length=255, blank=True, null=True)
    github = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# অটোমেটিক প্রোফাইল তৈরির সিগন্যাল (ইউজার রেজিস্ট্রেশন করলে প্রোফাইল তৈরি হবে)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# ---------------------------------------------------
# ২. আপলোড করা অ্যাপ/কন্টেন্ট মডেল
# ---------------------------------------------------
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
    
    # অ্যাপের লোগো বা আইকন
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    downloads = models.IntegerField(default=0)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)
    total_votes = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False) # অ্যাডমিন চেক করলে এটি True হবে

    def __str__(self):
        return f"{self.title} - {self.content_type} (by {self.uploaded_by.username})"


# ---------------------------------------------------
# ৩. অ্যাপ রিকোয়েস্ট মডেল
# ---------------------------------------------------
class AppRequest(models.Model):
    app_name = models.CharField(max_length=200)
    description = models.TextField()
    user_email = models.EmailField(blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.app_name