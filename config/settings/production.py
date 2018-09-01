from .shared import (
    BASE_DIR,
    PROJ_DIR,
    INSTALLED_APPS,
    MIDDLEWARE,
    ROOT_URLCONF,
    TEMPLATES,
    WSGI_APPLICATION,
    DATABASES,
    AUTH_PASSWORD_VALIDATORS,
    LANGUAGE_CODE,
    TIME_ZONE,
    USE_I18N,
    USE_L10N,
    USE_TZ,
    STATIC_URL,
    STATICFILES_DIRS,
    STATIC_ROOT,
    env,
    APPEND_SLASH,
    LOGOUT_REDIRECT_URL,
    list_of_tuples,
    AUTH_USER_MODEL,
    LOGIN_URL,
)

__all__ = [
    'BASE_DIR',
    'PROJ_DIR',
    'SECRET_KEY',
    'DEBUG',
    'ALLOWED_HOSTS',
    'INSTALLED_APPS',
    'MIDDLEWARE',
    'ROOT_URLCONF',
    'WSGI_APPLICATION',
    'DATABASES',
    'AUTH_PASSWORD_VALIDATORS',
    'LANGUAGE_CODE',
    'TIME_ZONE',
    'USE_I18N',
    'USE_L10N',
    'USE_TZ',
    'STATIC_URL',
    'STATICFILES_DIRS',
    'STATIC_ROOT',
    'APPEND_SLASH',
    'LOGOUT_REDIRECT_URL',
    'AUTH_USER_MODEL',
    'LOGIN_URL',
]

DEBUG = False
DATABASES['default'] = env.db('DATABASE_URL')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
EMAIL_BACKEND = 'sparkpost.django.email_backend.SparkPostEmailBackend'
SPARKPOST_API_KEY = env('SPARKPOST_API_KEY')
ADMINS = env('ADMINS', cast=list_of_tuples)
DEFAULT_FROM_EMAIL = 'no-reply@library.qiime2.org'
SERVER_EMAIL = 'no-reply@library.qiime2.org'
EMAIL_HOST = 'library.qiime2.org'
EMAIL_SUBJECT_PREFIX = '[library.qiime2.org] '
DISCOURSE_SSO_PROVIDER = 'forum.qiime2.org'
DISCOURSE_SSO_SECRET = env('DISCOURSE_SSO_SECRET')
GOOGLE_ANALYTICS_PROPERTY_ID = env('GOOGLE_ANALYTICS_PROPERTY_ID')
TEMPLATES[0]['OPTIONS']['context_processors'].append('library.utils.context_processors.google_analytics')
