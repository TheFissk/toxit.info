from pathlib import Path
import os
from urllib.parse import urlparse
from google.cloud import secretmanager

def fetch_secret(secret_id):
    '''
    This utility function returns a secret payload at runtime using the secure google secrets API 
    '''
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/mhs-reddit/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Security Settings
SECRET_KEY = fetch_secret('django_secret_key')
DEBUG = True

# CSRF Protection
if 'CLOUDRUN_SERVICE_URL' in os.environ:
    CLOUDRUN_SERVICE_URL = os.environ['CLOUDRUN_SERVICE_URL']

if 'PUBLIC_URL' in os.environ:
    PUBLIC_URL = os.environ['PUBLIC_URL']

if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc, urlparse(PUBLIC_URL).netloc ]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL, PUBLIC_URL]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    ALLOWED_HOSTS = ['.localhost']

# Application definition
INSTALLED_APPS = [
    'toxit.apps.ToxitConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'toxit_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'toxit_main.wsgi.application'


# Database 
if 'DB_HOST_ADDR' in os.environ:
    db_host = os.environ['DB_HOST_ADDR']
else:
    db_host = 'localhost'

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mhs-init',
        'USER': fetch_secret('mhs_prod_db_username'),
        'PASSWORD': fetch_secret('mhs_prod_db_password'),
        'HOST': db_host,
        'PORT': '5432',
    }
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Canada/Saskatchewan'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
if 'GS_BUCKET_NAME' in os.environ:
    GS_BUCKET_NAME = os.environ['GS_BUCKET_NAME']
GS_PROJECT_ID = 'mhs-reddit'
STATIC_URL = '/static/'
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_DEFAULT_ACL = 'publicRead'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]