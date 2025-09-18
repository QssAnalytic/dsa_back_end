from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5=o5z-&u=2!8q2grbogelvj&a^+r7(+kq#w^%3%4!lr%edjh()'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

APPEND_SLASH = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 31536000  # 1 il
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"


# Allowed hosts for your backend
ALLOWED_HOSTS = ['dsabackend-production-00f4.up.railway.app', '127.0.0.1']

# Trusted origins for CSRF (important for POST requests or forms)
CSRF_TRUSTED_ORIGINS = [
    "https://dsabackend-production-00f4.up.railway.app",
    "https://dsafrontend-production.up.railway.app",  # Add your frontend domain
    "https://dsaadmin-production.up.railway.app",
    "http://localhost:5174",
    "https://new.dsa.az",
    "https://news.dsa.az"
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sslserver',
    'main',  # Your app
    'corsheaders',  # For handling CORS
    'rest_framework',  # For Django REST Framework
    'storages',  # AWS S3 için django-storages eklendi
]

# Middleware configuration
# Ensure CorsMiddleware is before CommonMiddleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Moved to the top for CORS processing
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False  # Don't allow all origins
CORS_ALLOWED_ORIGINS = [
    "https://dsafrontend-production.up.railway.app",
    "https://dsaadmin-production.up.railway.app",
    "http://localhost:3000",
    "http://localhost:5174",
    "https://new.dsa.az",
    "https://news.dsa.az"
]

# Allow specific HTTP methods for CORS requests
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Allow specific headers in CORS requests
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "cache-control",
]
# Set to True if your frontend sends cookies or authentication headers
CORS_ALLOW_CREDENTIALS = False  # Change to True if needed

# URL configuration
ROOT_URLCONF = 'dsa.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'dsa.wsgi.application'

# Database configuration (using Railway's DATABASE_URL)
DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Superuser configuration (optional, for admin user creation)
SUPERUSER_USERNAME = os.getenv('SUPERUSER_USERNAME')
SUPERUSER_EMAIL = os.getenv('SUPERUSER_EMAIL')
SUPERUSER_PASSWORD = os.getenv('SUPERUSER_PASSWORD')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (uploads) - Artık S3 kullanılacak, bu yüzden MEDIA_ROOT kaldırıldı
MEDIA_URL = 'https://dsa-media-img.s3.amazonaws.com/'  # S3 bucket URL'niz
MEDIA_ROOT = ''

# AWS S3 Ayarları
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'dsa-media-img'
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = None

# Medya dosyaları için S3'ü varsayılan depolama yapın
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# İsteğe bağlı: Dosyaların üzerine yazılmasını engellemek için
AWS_S3_FILE_OVERWRITE = False

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
