from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.splash_screen, name='splash'),
    path('home/', views.home, name='home'),
    path('upload/', views.upload_content, name='upload'),
    path('update-rating/', views.update_rating, name='update_rating'),
    
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # নতুন যোগ করা হলো
    path('dashboard/', views.dashboard, name='dashboard'),
    path('app/<int:pk>/', views.app_detail, name='app_detail'),
    path('customer-care/', views.customer_care, name='customer_care'),
    path('download/<int:pk>/', views.download_file, name='download_file'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('trending/', views.trending_apps, name='trending'),
    path('developer/<str:username>/', views.developer_profile, name='developer_profile'),
    path('faq/', views.faq_view, name='faq'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('changelog/', views.changelog_view, name='changelog'),
    path('request-app/', views.app_request_view, name='app_request'),
]