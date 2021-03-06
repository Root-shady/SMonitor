"""
Django settings for SMonitor project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
SECRET_KEY = os.environ.get('SECRET_KEY', 'unknow')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party app
    'rest_framework',

    # self-defined apps
    'account',
    'rolepermission',
    'system',
    'projectlog',
    'server',
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

ROOT_URLCONF = 'Config.urls'
AUTH_USER_MODEL = 'account.User'
AUTHENTICATION_BACKENDS = ['account.authbackend.EmailOrUsernameModelBackend',]


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

WSGI_APPLICATION = 'Config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('NAME', 'unknown'),
        'USER': os.environ.get('USER', 'unconfigure'),
        'PASSWORD': os.environ.get('PASSWORD', 'secret'),
        'HOST': os.environ.get('HOST', 'localhost'),
        'PORT': os.environ.get('PORT', '3306')
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# System File management
STATIC_URL = '/Static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'collectstatic', 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'collectstatic', 'media_root')

STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'Static'),
    )

# Email Sending Settings
EFAULT_FROM_EMAIL = os.environ.get('EFAULT_FROM_EMAIL', 'Unconfigure') 
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'Unconfigure')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smp')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '25')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'email')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'password')
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'backend setting')

# Configuration
HOST = ''
ACTIVATION = False
PASSWORDCHECK = False
