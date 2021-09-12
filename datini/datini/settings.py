from pathlib import Path
import os

from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = os.environ['DJANGO_DEBUG'] == "1"

ALLOWED_HOSTS = []
defined_hostname = os.environ.get('HOSTNAME')
if defined_hostname:
    ALLOWED_HOSTS = [defined_hostname]
if DEBUG:
    ALLOWED_HOSTS.append("localhost")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djmoney',
    'tracker'
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

ROOT_URLCONF = 'datini.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': False,
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

WSGI_APPLICATION = 'datini.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': Path(os.environ['DJANGO_DBDATA_ROOT']) / "datini.sqlite3.db",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = os.environ['DJANGO_STATIC_URL']
STATIC_ROOT = os.environ['DJANGO_STATIC_ROOT']
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIA_URL = os.environ['DJANGO_MEDIA_URL']
MEDIA_ROOT = os.environ['DJANGO_MEDIA_ROOT']

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

# Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = "/login"
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'tracker.User'

# Logging configuration
# https://docs.djangoproject.com/en/3.1/topics/logging/#configuring-logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': DEFAULT_LOGGING['filters'],
    "formatters": {
        "standard": {
            "format": '%(asctime)s %(name)s %(levelname)s %(message)s'
        },
        **DEFAULT_LOGGING['formatters']
    },
    'handlers': {
        'datini': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'filename': Path(os.environ['DJANGO_LOG_ROOT']) / 'datini.log',
            'formatter': 'standard',
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1048576,  # 1MB
            "backupCount": 5
        },
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'filename': Path(os.environ['DJANGO_LOG_ROOT']) / 'django.log',
            'formatter': 'standard',
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1048576,  # 1MB
            "backupCount": 5
        },
        **DEFAULT_LOGGING['handlers']
    },
    'loggers': {
        'django': {
            'handlers': ['django', 'mail_admins'],
            'level': 'INFO'
        },
        'datini': {
            'handlers': ['datini'],
            'level': 'DEBUG',
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server']
    },
}

# https://docs.djangoproject.com/en/3.1/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Email send configuration
# https://docs.djangoproject.com/en/3.2/topics/email/#smtp-backend
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = "no-reply@datini.eu"
DEFAULT_FROM_EMAIL = "no-reply@datini.eu"

# Admins email
ADMINS = []
admin_names = os.environ.get('ADMIN_NAMES')
admin_email_addresses = os.environ.get('ADMIN_EMAIL_ADDRESSES')
if admin_names and admin_email_addresses:
    ADMINS = [(name.strip(), addr.strip()) for name, addr in zip(admin_names.split(","), admin_email_addresses.split(","))]
