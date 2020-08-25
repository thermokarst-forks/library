web: gunicorn config.wsgi:application
worker: celery worker -A config.celery --loglevel=info -Q default --hostname=dokku@%h
flower: celery flower -A config.celery --address=0.0.0.0 --port=5555
