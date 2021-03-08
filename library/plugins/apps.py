# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.apps import AppConfig


class PluginsConfig(AppConfig):
    name = 'library.plugins'

    def ready(self):
        # register the decorated signals
        from . import signals  # noqa: F401
