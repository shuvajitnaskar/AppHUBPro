from django.urls import path, include
from . import views

urlpatterns = [
    # স্প্ল্যাশ স্ক্রিন (সবার আগে এটি দেখাবে)
    path('', views.splash_screen, name='splash'),
    
    # হোম পেজ
    path('home/', views.home, name='home'),
    
    # রেটিং আপডেট করার জন্য
    path('update-rating/', views.update_rating, name='update_rating'),
    
    # কন্টেন্ট বা APK আপলোড করার জন্য
    path('upload/', views.upload_content, name='upload'),
    
    # নতুন অ্যাকাউন্ট খোলার জন্য (Registration)
    path('register/', views.register, name='register'),
    
    # লগ-ইন এবং লগ-আউট অটো হ্যান্ডেল করার জন্য
    path('accounts/', include('django.contrib.auth.urls')),
]