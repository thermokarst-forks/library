# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from celery import Celery


app = Celery('library-tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
