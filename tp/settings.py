from pathlib import Path
from .logging_settings import init_logging_settings
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if str(os.getenv('DEBUG')) == "True" else False

ALLOWED_HOSTS = [x for x in os.environ.get('ALLOWED_HOSTS').split(' ')]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'crispy_forms',
    'audio.apps.AudioConfig',
    'accounts.apps.AccountsConfig',
    'storages',
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

ROOT_URLCONF = 'tp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['tp/templates'],
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

WSGI_APPLICATION = 'tp.wsgi.application'

LOGGING_XMPP_CONFIG = {
    'LOGGING_XMPP_SERVER': str(os.getenv('LOGGING_XMPP_SERVER')),
    'LOGGING_XMPP_SENDER': str(os.getenv('LOGGING_XMPP_SENDER')),
    'LOGGING_XMPP_PASSWORD': str(os.getenv('LOGGING_XMPP_PASSWORD')),
    'LOGGING_XMPP_RECIPIENT': str(os.getenv('LOGGING_XMPP_RECIPIENT')),
    'LOGGING_XMPP_COMMAND': str(os.getenv('LOGGING_XMPP_COMMAND')),
    'LOGGING_XMPP_USE_TLS': str(os.getenv('LOGGING_XMPP_USE_TLS'))
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = '/static/'

# aws settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_DEFAULT_ACL = None
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# s3 static settings
STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'tp.storage_backends.StaticStorage'
# s3 public media settings
PUBLIC_MP3_LOCATION = 'mp3'
MP3_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MP3_LOCATION}/'
MP3_FILE_STORAGE = 'tp.storage_backends.PublicMP3Storage'
PUBLIC_IMAGES_LOCATION = 'images'
IMAGES_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_IMAGES_LOCATION}/'
IMAGES_FILE_STORAGE = 'tp.storage_backends.PublicImageStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
LOGGING = init_logging_settings()

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == "True"
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DOMAIN_NAME = os.getenv('DOMAIN_NAME')
