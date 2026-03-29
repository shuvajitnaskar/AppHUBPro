from django.contrib import admin
from .models import UploadedContent

# আমাদের তৈরি করা ডেটাবেস টেবিলটি অ্যাডমিন প্যানেলে যুক্ত করা হলো
admin.site.register(UploadedContent)