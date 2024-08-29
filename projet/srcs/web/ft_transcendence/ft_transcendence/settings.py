"""
Django settings for ft_transcendence project.

Generated by 'django-admin startproject' using Django 3.2.25.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l940snh=!msg^xy)=^q4@*n08szdxjy+hhm)-)vwei4cuyn9x('

# 42 API informations
CLIENT_ID_42 = os.getenv('UID_42')
CLIENT_SECRET_42 = os.getenv('SECRET_42')

# A2F information

SENDER_A2F = os.getenv('SENDER_A2F')
PASSWORD_A2F = os.getenv('PASSWORD_A2F')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
	'localhost',
	'127.0.0.1',
	'[::1]',
	'django'
]

INTERNAL_IPS = [
	"localhost",
	'django',
	"127.0.0.1",
]

import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]

DEBUG_TOOLBAR_CONFIG = {
	'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

# Application definition

INSTALLED_APPS = [
	'daphne',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_prometheus',
	'debug_toolbar',
	'shortuuid',
	'home',
	'user_manage',
	'live_chat',
	'pong_game',
	'tournament',
	'pyotp',
]

MIDDLEWARE = [
	'django_prometheus.middleware.PrometheusBeforeMiddleware',

	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',

	'debug_toolbar.middleware.DebugToolbarMiddleware',
	'django_htmx.middleware.HtmxMiddleware',

	'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'ft_transcendence.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'logstash',
            'port': 5044,
            'version': 1,
            'message_type': 'django',
            'fqdn': False,
            'tags': ['django'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logstash', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# WSGI_APPLICATION = 'ft_transcendence.wsgi.application'
ASGI_APPLICATION = 'ft_transcendence.asgi.application'

CHANNEL_LAYERS = {
        'default': {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.getenv('POSTGRES_DB'),
		'USER': os.getenv('POSTGRES_USER'),
		'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
		'HOST': 'postgresql',
		'POST': '5432'
	}
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'user_manage.CustomUser'

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
