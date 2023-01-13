from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-l7rgj_+zs0z%$j4kd018z=qyy5@)4!8wzq$ki82bua3ral!(%v'
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "bmw",
    "schedule",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "widget_tweaks"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fugro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fugro.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "railway",
        "USER": "postgres",
        "PASSWORD": "7mdYeOtRQxFW05ri8UZC",
        "HOST": "containers-us-west-119.railway.app",
        "PORT": "7783"
    }
}

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
TIME_ZONE = 'CET'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CSRF_TRUSTED_ORIGINS = ["https://development-production.up.railway.app"]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"