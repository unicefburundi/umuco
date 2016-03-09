"""
Django settings for turabeneza project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse_lazy
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yz@q%2pw2s%#v48)9#5r=za$zv!ho3v^wt0u--wws)3o*+*+n)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_tables2',
    'djcelery',
    'import_export',
    'umuco',
    'authtools',
    'bdiadmin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'umuco_main.urls'

WSGI_APPLICATION = 'umuco_main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Bujumbura'

USE_I18N = True

USE_L10N = True

USE_TZ = True

KNOWN_PREFIXES = {
    'RG':'PHONE_REGISTRATION',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

STATIC_ROOT =  os.path.join(BASE_DIR, "static")

MEDIA_ROOT = BASE_DIR + '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

# Django-authtools
AUTH_USER_MODEL = 'authtools.User'

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
PASSWORD = '12ab'
CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'

INTERNAL_IPS = '127.0.0.1'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'youremail@gmail.com'

EMAIL_HOST_PASSWORD = 'abcdefghijklmnopqr'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

SITE_ID = 1

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#-----------------------------------------------------------------------------------
# Login / Logout
#-----------------------------------------------------------------------------------
LOGIN_URL = reverse_lazy("login")
LOGOUT_URL = reverse_lazy("logout")
LOGIN_REDIRECT_URL = reverse_lazy("analytics")
LOGOUT_REDIRECT_URL = reverse_lazy("home")

TOKEN = 'rapidprotoken'

# Django extensions
try:
    import django_extensions
except ImportError:
    pass
else:
    INSTALLED_APPS = INSTALLED_APPS + ('django_extensions',)


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError:
    pass
