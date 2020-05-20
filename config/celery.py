from celery import Celery


app = Celery('library-tasks', backend='rpc://', broker='amqp://')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
