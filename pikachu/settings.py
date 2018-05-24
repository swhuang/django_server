# -*- coding: utf-8 -*-
"""
Django settings for pikachu project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from __future__ import absolute_import
import os
import djcelery
import siteuser
import platform

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tiz+&t3)%9-!s*ia&0l!9q=cb2k4o8vbjphglrffnk@a)=wjxe'

# SECURITY WARNING: don't run with debug turned on in production!
if platform.system() == 'Darwin':
    DEBUG = True
    # DOMAIN = 'http://120.55.55.106:3306'
    DOMAIN = 'http://localhost:3306'
    # CACHES_BACKEND = 'django.core.cache.backends.memcached.MemcachedCache'
    # host = '120.55.55.106'
    host = 'localhost'
    port = '3306'
    name = 'root'
    pwd = 'vq8612VQE'
    db_name = 'cms'
else:
    DEBUG = False
    # DOMAIN = 'http://120.55.55.106:3306'
    DOMAIN = 'rm-bp1h06uw3zk7a18x2.mysql.rds.aliyuncs.com:3306'
    # CACHES_BACKEND = 'django.core.cache.backends.memcached.MemcachedCache'
    # host = '120.55.55.106'
    host = 'rm-bp1h06uw3zk7a18x2.mysql.rds.aliyuncs.com'
    port = '3306'
    name = 'root'
    pwd = 'vq8612VQE'
    db_name = 'cms'

ALLOWED_HOSTS = ['*', ]

from os import environ

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': db_name,  # Or path to database file if using sqlite3.
        'USER': name,  # Not used with sqlite3.
        'PASSWORD': pwd,  # Not used with sqlite3.
        'HOST': host,  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': port,  # Set to empty string for default. Not used with sqlite3.
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crm',
    'Accounting',
    'users',
    'easy_pjax',
    'commom',
    'djcelery',
    'periodic',
    'siteuser.member',
    'siteuser.notify',
    'easy_thumbnails',
    'django_filters',
    'FP_risk',
    'rest_framework',
    'gunicorn',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 2,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
AUTH_USER_MODEL = 'users.User'
SITEUSER_EXTEND_MODEL = 'users.models.ExtendMember'
SITEUSER_ACCOUNT_MIXIN = 'crm.crmmember.mem_custom.AccountMxin'
SITEUSER_EMAIL = {
    'smtp_host': 'smtp.163.com',
    'smtp_port': 25,
    'username': 'superhsw',
    'password': '5961815949',
    'from': 'superhsw@gmail.com',
    'display_from': '',
}
AVATAR_DIR = 'crm/data'

USERS_PASSWORD_POLICY = {
    'UPPER': 0,  # Uppercase 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    'LOWER': 0,  # Lowercase 'abcdefghijklmnopqrstuvwxyz'
    'DIGITS': 0,  # Digits '0123456789'
    'PUNCTUATION': 0  # Punctuation """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'siteuser.middleware.User',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'pikachu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [siteuser.SITEUSER_TEMPLATE, 'django_filters.templates',
                 os.path.join(BASE_DIR, 'vue-pages/admin')],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': [
                'easy_pjax.templatetags.pjax_tags'
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'siteuser.context_processors.social_sites'
            ],
        },
    },
]

WSGI_APPLICATION = 'pikachu.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6
        },
    },

]


BACK_VALIDATORS = [
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

# Add Caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session_redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
    }
}

# add session engine
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session_redis"

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'vue-pages/admin/static'),
    os.path.join(BASE_DIR, "static"),
    '/siteuser/member/static',
)

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (200, 200), 'crop': True},
    },
}
# DEFAULT_CHARSET = 'GBK'
DEFAULT_CHARSET = 'UTF-8'

USERS_EMAIL_DOMAINS_BLACKLIST = []

USERS_EMAIL_DOMAINS_WHITELIST = []

USERS_REGISTRATION_OPEN = True

USERS_VERIFY_EMAIL = False

USERS_AUTO_LOGIN_ON_ACTIVATION = True

USERS_EMAIL_CONFIRMATION_TIMEOUT_DAYS = 3

USERS_AUTO_LOGIN_AFTER_REGISTRATION = True

# Specifies minimum length for passwords:
USERS_PASSWORD_MIN_LENGTH = 5

# Specifies maximum length for passwords:
USERS_PASSWORD_MAX_LENGTH = None

# the complexity validator, checks the password strength
USERS_CHECK_PASSWORD_COMPLEXITY = True

USERS_SPAM_PROTECTION = False  # important!

USERS_CREATE_SUPERUSER = True
USERS_SUPERUSER_NAME = 'admin'
USERS_SUPERUSER_EMAIL = 'superhsw@163.com'
USERS_SUPERUSER_PASSWORD = 'vq8612VQE'

LOGIN_REDIRECT_URL = '/userform/form/'

LGOIN_URL = '/accounts/login/'

DEFAULT_MERCHANT = '100000000000001'
DEFAULT_MERCHANT_ID = 1
# timely task
from celery.schedules import crontab

djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/1'

from datetime import timedelta

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] {<%(filename)s> <%(funcName)s> [%(lineno)d]} %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'monitor.log',
            'formatter': 'verbose'
        },
        'email': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'email'],
            'level': 'INFO',
            'propagate': True,
        },
        'batch': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

'''
CELERYBEAT_SCHEDULE = {
    'add-every-3-seconds': {
        'task': 'periodic.tasks.test_celery',
        # 'schedule': crontab(minute=u'40', hour=u'17',),
        'schedule': timedelta(seconds=3),
        'args': (16, 16)
    },
    'add-every-4-seconds': {
        'task': 'periodic.tasks.test_multiply',
        # 'schedule': crontab(minute=u'40', hour=u'17',),
        'schedule': timedelta(seconds=4),
        'args': (16, 16)
    },
    'add-every-2-seconds': {
        'task': 'periodic.tasks.test_do_order',
        # 'schedule': crontab(minute=u'40', hour=u'17',),
        'schedule': timedelta(seconds=2),
        'args': (16, 16)
    },
}
'''
