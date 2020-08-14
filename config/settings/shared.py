import os

import environ


env = environ.Env()


def list_of_tuples(var):
    return [tuple(p.split(',')) for p in var.split(';')]


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROJ_DIR = os.path.join(BASE_DIR, 'library')
SECRET_KEY = env('SECRET_KEY',
                 default='ou$@l5=z0h#^l!or)35eyf6wcb2y%+=1vik%f(ww^=++$apsab')
DEBUG = env('DEBUG', default=True)
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_celery_results',

    # utils needs to be registered for template tags, and needs to come first
    # because other apps use it
    'library.utils.apps.UtilsConfig',
    'library.plugins.apps.PluginsConfig',
    'library.users.apps.UsersConfig',
    'library.api.apps.APIConfig',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJ_DIR, 'templates')],
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
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://postgres@db:5432/postgres'),
}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # noqa: E501
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},  # noqa: E501
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  # noqa: E501
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  # noqa: E501
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
# Note that these paths should use Unix-style forward slashes, even on Windows
STATICFILES_DIRS = ['%s/static' % PROJ_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
APPEND_SLASH = True  # This is the default, but just want make it explicit
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = 'index'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ADMINS = env('ADMINS', default=list_of_tuples('x,x@x.com;y,y@y.com'),
             cast=list_of_tuples)
AUTH_USER_MODEL = 'users.User'
RABBITMQ_URL = env('RABBITMQ_URL', default='amqp://guest@mq')
# We want to use the rmq url set by dokku, emulating in dev
CELERY_BROKER_URL = env('RABBITMQ_URL', default='amqp://guest@mq')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_ROUTES = {
    'index.*': {'queue': 'default'},
    'packages.*': {'queue': 'packages'},
}
GITHUB_TOKEN = env('GITHUB_TOKEN', default='nope')
# TODO: set up django db celery backend
