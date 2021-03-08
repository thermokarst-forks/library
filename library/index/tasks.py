# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from celery.decorators import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task(name='index.debug')
def debug(payload):
    logger.info('Debug: %r' % (payload, ))
    return payload
