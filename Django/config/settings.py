__author__ = "Simon Nilsson"
__copyright__ = "Copyright 2017, Axenu"
__license__ = "GNU"
__version__ = "0.1"
__maintainer__ = "Simon Nilsson"
__email__ = "simon@axenu.com"
__status__ = "Development"

import os

from kombu import Exchange, Queue
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-2uhrhoxl(n)w3d0jp$ng9-pdesn63m8yyf&5pcky-vro+on!j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

#Custom settings: Store in database?
# PAKAGE_SEARCH_PATH = '/mnt/epp'
# if DEBUG:
#     PAKAGE_SEARCH_PATH = '/code/test_packages'
# PACKAGE_IN_PROGRESS_PATH = os.path.join(BASE_DIR, 'workdir')
# django-background-tasks
MAX_ATTEMPTS = 0



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'background_task',
    # 'core',
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    #     'rest_framework.authentication.BasicAuthentication',
    # ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# AUTH_USER_MODEL = 'api.User'
ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# if DEBUG:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': os.environ.get('DB_ENV_DB', 'postgres'),
    #     'USER': os.environ.get('DB_ENV_POSTGRES_USER', 'postgres'),
    #     'PASSWORD': os.environ.get('DB_ENV_POSTGRES_PASSWORD', 'postgres'),
    #     'HOST': os.environ.get('DB_PORT_5432_TCP_ADDR', 'db-workers'),
    #     'PORT': os.environ.get('DB_PORT_5432_TCP_PORT', ''),
    # },
    # 'default':{
    #    'ENGINE':'django.db.backends.postgresql_psycopg2',
    #    'USER':'saw',
    #    'PASSWORD':'pass',
    #    'HOST':'db',
    #    'NAME':'saw_db',
    #    'PORT':5432,
    # }
}
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         }
#         # 'default':{
#         #    'ENGINE':'django.db.backends.postgresql_psycopg2',
#         #    'USER':'saw',
#         #    'PASSWORD':'pass',
#         #    'HOST':'db',
#         #    'NAME':'saw_db',
#         #    'PORT':5432,
#         # }
#     }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# if DEBUG:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': os.path.join(BASE_DIR, "log/all.log"),
        # },
        # 'background': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': os.path.join(BASE_DIR, "log/background.log"),
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'background_task': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
# else:
#     LOGGING = {
#         'version': 1,
#         'disable_existing_loggers': False,
#         'handlers': {
#             'file': {
#                 'level': 'DEBUG',
#                 'class': 'logging.FileHandler',
#                 'filename': os.path.join(BASE_DIR, "log/all.log"),
#             },
#             'background': {
#                 'level': 'DEBUG',
#                 'class': 'logging.FileHandler',
#                 'filename': os.path.join(BASE_DIR, "log/background.log"),
#             },
#         },
#         'loggers': {
#             'django': {
#                 'handlers': ['file'],
#                 'level': 'INFO',
#                 'propagate': True,
#             },
#             'background_task': {
#                 'handlers': ['background'],
#                 'level': 'DEBUG',
#                 'propagate': True,
#             },
#         },
#     }

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "statichtml")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
    # os.path.join(BASE_DIR, "aurelia/static"),
    os.path.join(BASE_DIR, "static/angular"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")


# Redis
#
# REDIS_PORT = 6379
# REDIS_DB = 0
# REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')
#
# RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')
#
# if RABBIT_HOSTNAME.startswith('tcp://'):
#     RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]
#
# BROKER_URL = os.environ.get('BROKER_URL',
#                             '')
# if not BROKER_URL:
#     BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
#         user=os.environ.get('RABBIT_ENV_USER', 'admin'),
#         password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'mypass'),
#         hostname=RABBIT_HOSTNAME,
#         vhost=os.environ.get('RABBIT_ENV_VHOST', ''))
#
# # We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
# BROKER_HEARTBEAT = '?heartbeat=30'
# if not BROKER_URL.endswith(BROKER_HEARTBEAT):
#     BROKER_URL += BROKER_HEARTBEAT
#
# BROKER_POOL_LIMIT = 1
# BROKER_CONNECTION_TIMEOUT = 10
#
# # Celery configuration
#
# # configure queues, currently we have only one
# CELERY_DEFAULT_QUEUE = 'default'
# CELERY_QUEUES = (
#     Queue('default', Exchange('default'), routing_key='default'),
# )
#
# # Sensible settings for celery
# CELERY_ALWAYS_EAGER = False
# CELERY_ACKS_LATE = True
# CELERY_TASK_PUBLISH_RETRY = True
# CELERY_DISABLE_RATE_LIMITS = False
#
# # By default we will ignore result
# # If you want to see results and try out tasks interactively, change it to False
# # Or change this setting on tasks level
# CELERY_IGNORE_RESULT = True
# CELERY_SEND_TASK_ERROR_EMAILS = False
# CELERY_TASK_RESULT_EXPIRES = 600
#
# # Set redis as celery result backend
# CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)
# CELERY_REDIS_MAX_CONNECTIONS = 1
#
# # Don't use pickle as serializer, json is much safer
# CELERY_TASK_SERIALIZER = "json"
# CELERY_ACCEPT_CONTENT = ['application/json']
#
# CELERYD_HIJACK_ROOT_LOGGER = False
# CELERYD_PREFETCH_MULTIPLIER = 1
# CELERYD_MAX_TASKS_PER_CHILD = 1000
#
#
# #JWT
#
# JWT_AUTH = {
#     'JWT_ALLOW_REFRESH': True,
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=7200),
# }
