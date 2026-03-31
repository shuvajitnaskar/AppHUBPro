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
]