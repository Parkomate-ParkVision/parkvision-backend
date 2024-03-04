from pathlib import Path
from dotenv import load_dotenv
import os
import datetime
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOGS_DIR = os.path.join(BASE_DIR, 'logs')
API_LOG_DIR = os.path.join(LOGS_DIR, "api")
GUNICORN_LOG_DIR = os.path.join(LOGS_DIR, 'gunicorn')
CELERY_LOG_DIR = os.path.join(LOGS_DIR, 'celery')
EXCEPTION_LOG_DIR = os.path.join(LOGS_DIR, "exceptions")

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)
    os.mkdir(API_LOG_DIR)
    os.mkdir(GUNICORN_LOG_DIR)
    os.mkdir(CELERY_LOG_DIR)
    os.mkdir(EXCEPTION_LOG_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-rvt_u0uc(p-c@hbj(hm)o^7(ja%l@tf^v1k1dsadm6(2m+osjv"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_api_logger",
    "rest_framework",
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    'django_extensions',
    "corsheaders",
    "phonenumber_field",
    'rest_framework_swagger',
    'drf_yasg',
    "analytics",
    "organization",
    "parking",
    "users",
    "vehicle",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]

# Logging settings
DRF_API_LOGGER_DATABASE = True

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASS"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

CELERY_BROKER_URL = 'amqp://admin:admin@parkomate-rabbitmq'

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "staticfiles"),
# ]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = [
#     "http://localhost:5173",
#     "http://localhost:3000",
#     "*",
# ]

AUTH_USER_MODEL = "users.ParkomateUser"

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-requested-with",
    "x-csrftoken",
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Methods",
    "Access-Control-Allow-Credentials",
    "ngrok-skip-browser-warning",
    "x-timezone-region"
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
