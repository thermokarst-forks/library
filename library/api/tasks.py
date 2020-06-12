from celery.decorators import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task(name='fetch_package_from_github')
def fetch_package_from_github(payload):
    logger.info('Debug: %r' % (payload, ))
    return payload
