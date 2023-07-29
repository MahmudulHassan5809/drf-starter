import os
from myproject.settings import BASE_DIR


AUTH_USER_MODEL = 'accounts.User'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myproject/static')
]


# Media settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DATABASE ENV
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT'))


# REDIS & CELERY ENV
REDIS_HOST = os.environ.get('REDIS_HOST')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 8))

# EMAIL ENV
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
FROM_EMAIL = os.environ.get('FROM_EMAIL')

# AWS ENV
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET')
S3_ENDPOINT = os.environ.get('S3_ENDPOINT')
AWS_REGION = os.environ.get('AWS_REGION')


# SSL SMS
SSL_SID = os.environ.get('SSL_SID')
SSL_TOKEN = os.environ.get('SSL_TOKEN')
SSL_URL = os.environ.get('SSL_URL')


# PROJECT
PROJECT_TITLE = os.environ.get('PROJECT_TITLE')
PROJECT_VERSION = os.environ.get('PROJECT_VERSION')

ENVIRONMENT = os.environ.get('ENVIRONMENT')
