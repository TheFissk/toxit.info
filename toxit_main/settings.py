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

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = fetch_secret('django_secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CLOUDRUN_SERVICE_URL = os.environ['CLOUDRUN_SERVICE_URL']
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
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': { fetch_secret('toxit_db_string') }
            }

# DATABASES = {
#     'default': {

#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'mhs-init',
#         'USER': 'agent',
#         'PASSWORD': 'Tempa$$',
#         'HOST': f'/cloudsql/mhs-reddit:northamerica-northeast2:mhs-db',
#         'PORT': '5432',
#     }
#     } 


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Canada/Saskatchewan'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
# empty directory needed in root for cross application static files, prevents warning: staticfiles.W004
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] 

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Define static storage via django-storages[google]
GS_PROJECT_ID = 'mhs-reddit'
GS_BUCKET_NAME = fetch_secret('toxit_bucket_name')
STATIC_URL = '/static/'
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_DEFAULT_ACL = 'publicRead'