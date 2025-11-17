"""
Django settings for quickflicks project.
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url   # <-- NEW


# -------------------------------------------------------------
# BASE PROJECT PATH
# -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------------------------------------
# SECURITY / DEBUG
# -------------------------------------------------------------
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-placeholder-key-change-in-production",
)

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    ".herokuapp.com",
    "127.0.0.1",
    "localhost",
]


# -------------------------------------------------------------
# INSTALLED APPS
# -------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "accounts",
    "movies",
]


# -------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "quickflicks.urls"


# -------------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "quickflicks.wsgi.application"


# -------------------------------------------------------------
# DATABASES
# -------------------------------------------------------------

# LOCAL DEVELOPMENT → SQLITE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# HEROKU PRODUCTION → POSTGRES
DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL:
    DATABASES["default"] = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )


# -------------------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -------------------------------------------------------------
# AUTHENTICATION BACKENDS (Email OR Username login)
# -------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "accounts.auth_backend.EmailOrUsernameBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# -------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -------------------------------------------------------------
# STATIC FILES (Heroku + Whitenoise)
# -------------------------------------------------------------
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# -------------------------------------------------------------
# MAILTRAP SMTP EMAIL CONFIG
# -------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST", default="sandbox.smtp.mailtrap.io")
EMAIL_PORT = config("EMAIL_PORT", default=2525, cast=int)

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@quickflicks.com")

EMAIL_FAIL_SILENTLY = False


# -------------------------------------------------------------
# LOGGING
# -------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}


# -------------------------------------------------------------
# API KEYS
# -------------------------------------------------------------
TMDB_API_KEY = config("TMDB_API_KEY", default="")

if not TMDB_API_KEY:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("TMDB_API_KEY is not set – TMDB features will be disabled.")
