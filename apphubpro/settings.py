import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-zm86l8pg#xs7j&76shkei7r3xkx#+&r6yn#zbk3xfkm@=jr(b='

# প্রোডাকশনে যাওয়ার সময় এটি False করে দেওয়া ভালো, তবে এখন debugging-এর জন্য True থাক।
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # এই লাইনটি এখানে বসবে
    'django.contrib.staticfiles',
    'cloudinary',          # এই লাইনটি এখানে বসবে
    'core',
   ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Static ফাইলের জন্য জরুরি
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'apphubpro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'apphubpro.wsgi.application'

# Database
# লাইভ PostgreSQL ডাটাবেস যুক্ত করা হলো
DATABASES = {
    'default': dj_database_url.parse('postgresql://apphub_db_user:du5DGUXFrYMmIpHMYwpXf6uwwgwnEERX@dpg-d75mmb0gjchc73erqus0-a.oregon-postgres.render.com/apphub_db')
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration (ছবি, অ্যাপ, কিউআর কোডের জন্য)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'dashboard'

# Cloudinary Configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'CLOUDINARY_URL=cloudinary://<your_api_key>:<your_api_secret>@dxf0xkwml',
    'API_KEY': '955543615472557',
    'API_SECRET': 'Tc5Q-h7_T14RR3pBGgcviZdTeqw'
}

# ডিফল্ট স্টোরেজ হিসেবে Cloudinary সেট করা
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'