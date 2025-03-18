from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts for your backend
ALLOWED_HOSTS = ['dsabackend-production-00f4.up.railway.app']

# Trusted origins for CSRF (important for POST requests or forms)
CSRF_TRUSTED_ORIGINS = [
    "https://dsabackend-production-00f4.up.railway.app",
    "https://dsafrontend-production.up.railway.app/",  # Add your frontend domain
    "https://dsaadmin-production.up.railway.app",  # Add the admin domain (if applicable)
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # Your app
    'corsheaders',  # For handling CORS
    'rest_framework',  # For Django REST Framework
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
    "https://dsafrontend-production.up.railway.app/",
    "https://dsaadmin-production.up.railway.app",
    "http://localhost:3000",
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
# Removed duplicate DATABASES definition
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
SUPERUSER_USERNAME = os.getenv('SUPERUSER_USERNAME', 'admin')
SUPERUSER_EMAIL = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
SUPERUSER_PASSWORD = os.getenv('SUPERUSER_PASSWORD', 'adminadmin')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
