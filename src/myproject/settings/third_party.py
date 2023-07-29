from myproject.settings import DEBUG, CELERY_BROKER_URL, CELERY_RESULT_BACKEND

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'base.apis.renderers.DefaultRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PAGINATION_CLASS': 'base.helpers.CustomPagination',
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    )
}


if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] + (
        'base.apis.renderers.OnlyRawBrowsableAPIRenderer',
    )
    SWAGGER_SETTINGS = {
        'DEFAULT_AUTO_SCHEMA_CLASS': 'base.apis.swagger.CustomSwaggerAutoSchema',
    }

if not DEBUG:
    REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'base.exceptions.custom_exception_handler'


CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_ALLOW_HEADER = [
    'username',
    'group',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_HEADERS = '*'
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
    }
}

# 5 minutes cache
CACHE_MIDDLEWARE_SECONDS = 300

# celery
CELERY_BROKER_URL = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TASK_DEFAULT_QUEUE = 'myproject.celery'
