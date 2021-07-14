# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def run_cmd(cmd):
    split_cmd = shlex.split(cmd)
    subprocess.run(split_cmd)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('broker_url', type=str)
        parser.add_argument('log_level', type=str)
        parser.add_argument('queues', type=str)

    def handle(self, *args, **options):
        broker_url = options['broker_url']
        log_level = options['log_level']
        queues = options['queues']

        args = (broker_url, log_level, queues)

        # close over args
        def restart_celery_worker():
            run_cmd('pkill -f "celery worker"')
            run_cmd(
                'celery -A config.celery -b %s '
                'worker --loglevel=%s -Q %s' % args
            )

        autoreload.run_with_reloader(restart_celery_worker)
