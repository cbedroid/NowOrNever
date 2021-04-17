import os
import mimetypes
import django_heroku
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRETKEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG",0)
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split(" ")

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "simple_history",
    "crispy_forms",
    "widget_tweaks",
    "core",
    "countrycuzzins",
    "users",
    "django_cleanup",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "nowornever.urls"

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

WSGI_APPLICATION = "nowornever.wsgi.application"

# Database
# https: // docs.djangoproject.com/en/3.0/ref/settings/  # databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.getenv("SQL_USER", "user"),
        "PASSWORD": os.getenv("SQL_PASSWORD", "password"),
        "HOST": os.getenv("SQL_HOST", "localhost"),
        "PORT": os.getenv("SQL_PORT", "5432"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://localhost:6379"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# To run behind HTTPS proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGIN_URL = "/account/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"



JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "NowOrNever Admin",
    # Title on the brand, and the login screen (19 chars max)
    "site_header": "NowOrNever",
    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    #"site_logo": "media/images/Now_Never_Logo.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to NowOrNever",
    # Copyright on the footer
    "copyright": "NoworNever LLC",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "users.User",
    # Custom icons for side menu apps/models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "account.emailaddress": "fas fa-envelope",
        "countrycuzzin.image": "fas photo",
        "core.subscription": "fas fa-id-card",
        "sites.site": "fas fa-globe",
        "socialaccount.socialaccount": "fa fa-thumbs-up",
        "socialaccount.socialtoken": "fas fa-coins",
        "socialaccount.socialapp": "fab fa-app-store-ios",
        "quiz.quiz": "fas fa-edit",
        "quiz.question": "fas fa-question-circle",
        "quiz.result": "fas fa-file-alt",
        "users.user": "fa fa-user",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
}


# Email service
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.getenv("SUPPORT_EMAIL_USER")
EMAIL_HOST_PASSWORD = os.getenv("SUPPORT_EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 5

# for static css file mimetype errors
mimetypes.add_type("text/css", ".css", True)
