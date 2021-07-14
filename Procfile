web: gunicorn config.wsgi:application
worker: celery worker -A config.celery --loglevel=info -Q default,db --hostname=worker01@library.qiime2.org
