# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.db.models.signals import pre_save
from django.dispatch import receiver

from library.utils import slug
from .models import LegacyPlugin


@receiver(pre_save, sender=LegacyPlugin)
def slug_handler(sender, instance, **kwargs):
    instance.slug = slug(instance, 'title', 'slug')
