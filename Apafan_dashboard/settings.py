"""
Django settings for Apafan_dashboard project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
import dotenv



dotenv.load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+c&hdj8-3))0yxg!gfre0_du!9#l&v!xhj5(goguv^f&w(d-h5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
AUTH_USER_MODEL = 'user.User'
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # project app
    'device',
    'hall',
    'mqtt',
    'report',
    'setting',
    'user',
    'web_socket',
    'permissions',
    'parameter',
    'versions',
    # installed app
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'guardian',
    'corsheaders',
    'django.contrib.gis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'Apafan_dashboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Token',),
}

WSGI_APPLICATION = 'Apafan_dashboard.wsgi.application'

ASGI_APPLICATION = "Apafan_dashboard.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (f'redis://:{os.getenv("REDIS_PASSWORD")}@{os.getenv("REDIS_ADDRESS")}:{os.getenv("REDIS_PORT")}/0')],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv("DATABASE_NAME"),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASS'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'Apafan_dashboard.authoraization.CustomAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1 * 3600

SWAGGER_ENABLE = True

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    "LOGIN_URL": "/api/user-auth/login",
    'UI_RENDERERS': [
        'Apafan_dashboard.rendrer.CustomJSONRenderer',
    ]
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

VERSION_PATH_TO_UPLOAD = "data/version/"

OBJECT_PERMISSION_MODEL = ['device', 'head', ]

ADMIN_USER_PERMISSIONS = ["hall", 'production', 'device', 'squad', 'head']

BASE_MQTT_SUBSCRIBE_TOPIC = os.getenv("BASE_MQTT_SUBSCRIBE_TOPIC")

BASE_MQTT_PUBLISH_TOPIC = os.getenv('BASE_MQTT_PUBLISH_TOPIC')

BASE_LOG_TOPIC = os.getenv('BASE_LOG_TOPIC')

MQTT_ADDRESS = str(os.getenv('MQTT_ADDRESS'))

MQTT_PORT = os.getenv('MQTT_PORT')

MQTT_USER = os.getenv('MQTT_USER')

MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

MQTT_TEMP_TOPIC = os.getenv('MQTT_TEMP_TOPIC')

MQTT_BASE_SEND_TOPIC = os.getenv('MQTT_BASE_SEND_TOPIC')

MQTT_DEVICE_PARAMETER_SEND_TOPIC = os.getenv('MQTT_DEVICE_PARAMETER_SEND_TOPIC')

MQTT_HEAD_PARAMETER_SEND_TOPIC = os.getenv('MQTT_HEAD_PARAMETER_SEND_TOPIC')

MQTT_DEVICE_PARAMETER_RECEIVE_TOPIC = os.getenv('MQTT_DEVICE_PARAMETER_RECEIVE_TOPIC')

MQTT_HEAD_PARAMETER_RECEIVE_TOPIC = os.getenv('MQTT_HEAD_PARAMETER_RECEIVE_TOPIC')

MQTT_DEVICE_PARAMETER_UPDATE_TOPIC = os.getenv('MQTT_DEVICE_PARAMETER_UPDATE_TOPIC')

MQTT_HEAD_PARAMETER_UPDATE_TOPIC = os.getenv('MQTT_HEAD_PARAMETER_UPDATE_TOPIC')

MQTT_TEMP_DEVICE_TOPIC = os.getenv('MQTT_TEMP_DEVICE_TOPIC')


GDAL_LIBRARY_PATH = r"D:\Work\Atibin\Server\apafan_dashboard\venv\Lib\site-packages\osgeo\gdal304.dll"
GEOS_LIBRARY_PATH = r"D:\Work\Atibin\Server\apafan_dashboard\venv\Lib\site-packages\osgeo\geos_c.dll"
# GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH', r'C:\OSGeo4W\bin\gdal309.dll')




