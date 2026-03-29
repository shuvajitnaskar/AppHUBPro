from django.urls import path
from . import views

urlpatterns = [
    path('', views.splash_screen, name='splash'),
    path('home/', views.home, name='home'),
    path('update-rating/', views.update_rating, name='update_rating'),
    path('upload/', views.upload_content, name='upload'),
]