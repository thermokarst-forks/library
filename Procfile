web: gunicorn config.wsgi:application
worker: celery worker -A config.celery --loglevel=info -Q default --hostname=dokku@%h
