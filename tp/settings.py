from pathlib import Path
from .logging_settings import init_logging_settings
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv('SECRET_KEY'))

DEBUG = True if str(os.getenv('DEBUG')) == "True" else False

ALLOWED_HOSTS = [x for x in os.environ.get('ALLOWED_HOSTS').split(' ')]

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
    'about.apps.AboutConfig',
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
                'django.template.context_processors.media',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_DOMAIN = os.getenv("STATIC_DOMAIN")
MP3_ROOT = os.path.join(BASE_DIR, 'media/audio/mp3')
IMAGE_ROOT = os.path.join(BASE_DIR, 'media/audio/images')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/audio')

STATIC_URL = f"{STATIC_DOMAIN}/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_URL = f"{STATIC_DOMAIN}/audio/"
IMAGES_URL = f"{MEDIA_URL}images/"
MP3_URL = f"{MEDIA_URL}mp3/"

LOGGING = init_logging_settings()

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == "True"
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DOMAIN_NAME = os.getenv('DOMAIN_NAME')
