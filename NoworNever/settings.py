"""
Django settings for NoworNever project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import mimetypes
from easy_thumbnails.conf import Settings as thumbnail_settings
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'f@b8j0!fe#pwqq_+ma($x^30l5#5wr(r&6p+_y2tg_mbpmxn57'
SECRET_KEY = os.environ.get("NON_SECRET_KEY")
if not SECRET_KEY:
    raise TypeError("Invalid or Missing Secret Key")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("NON_DEBUG") == "True"
DEBUG = False

if DEBUG:
    # for local testing: allowed hosts
    ALLOWED_HOSTS = [
        "127.0.0.1",
        "192.168.0.3",
        "192.168.0.2",
        "10.0.0.54",
        "192.168.0.5",
        "0.0.0.0:80",
    ]
else:
    ALLOWED_HOSTS = [
        "127.0.0.1",
        "192.168.0.3",
        "192.168.0.2",
        "10.0.0.54",
        "192.168.0.5",
        "0.0.0.0:80",
    ]

# Application definition
INSTALLED_APPS = [
    "countrycuzzins.apps.CountrycuzzinsConfig",
    "users.apps.UsersConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "widget_tweaks",
    "easy_thumbnails",
    "image_cropping",
]

# Image Cropping
THUMBNAIL_PROCESSORS = (
    "image_cropping.thumbnail_processors.crop_corners",
) + thumbnail_settings.THUMBNAIL_PROCESSORS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "NoworNever.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "NoworNever.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_INPUT_FORMATS = [
    "%I:%M:%S %p",  # 6:22:44 PM
    "%I:%M %p",  # 6:22 PM
    "%I %p",  # 6 PM
    "%H:%M:%S",  # '14:30:59'
    "%H:%M:%S.%f",  # '14:30:59.000200'
    "%H:%M",  # '14:30'
]


# Static
# https://docs.djangoproject.com/en/3.0/howto/static-files/

CRISPY_TEMPLATE_PACK = "bootstrap4"
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")
IMAGE_ROOT = os.path.join(MEDIA_ROOT, "images/")
AUDIO_ROOT = os.path.join(MEDIA_ROOT, "audio/")
VIDEO_ROOT = os.path.join(MEDIA_ROOT, "videos/")

LOGIN_URL = "/account/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"


# Email service
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("NON_SUPPORT_EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("NON_SUPPORT_EMAIL_PASS")

# for static css file mimetype errors
mimetypes.add_type("text/css", ".css", True)
