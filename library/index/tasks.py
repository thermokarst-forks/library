from celery.decorators import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task(name='index.debug')
def debug(payload):
    logger.info('Debug: %r' % (payload, ))
    return payload
