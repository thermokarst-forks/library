from celery.decorators import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task(name='debug_request')
def debug_request(request):
    logger.info('Request: %r' % (request, ))
