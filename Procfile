web: gunicorn config.wsgi:application
worker: celery -A config.celery worker --loglevel=info -Q default,db,periodic --hostname=worker01@library.qiime2.org
