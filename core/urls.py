from django.urls import path, include
from . import views

urlpatterns = [
    # ১. মেইন পেজ এবং স্প্ল্যাশ স্ক্রিন
    path('', views.splash_screen, name='splash'),
    path('home/', views.home, name='home'),
    
    # ২. ইউজার প্রোফাইল এবং রেজিস্ট্রেশন
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('developer/<str:username>/', views.developer_profile, name='developer_profile'),
    
    # ৩. অ্যাপ আপলোড এবং ডিটেইলস
    path('upload/', views.upload_content, name='upload'),
    path('app/<int:pk>/', views.app_detail, name='app_detail'),
    path('download/<int:pk>/', views.download_file, name='download_file'),
    
    # ৪. ফিচার্ড এবং অ্যানালিটিক্স
    path('trending/', views.trending_apps, name='trending'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    
    # ৫. ইন্টারঅ্যাকশন (Rating/Request)
    path('update-rating/', views.update_rating, name='update_rating'),
    path('request-app/', views.app_request_view, name='app_request'),
    
    # ৬. সাপোর্ট এবং পলিসি পেজ
    path('customer-care/', views.customer_care, name='customer_care'),
    path('faq/', views.faq_view, name='faq'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('changelog/', views.changelog_view, name='changelog'),
]