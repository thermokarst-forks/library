# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.utils.text import slugify


def slug(model_instance, slugable_field_name, slug_field_name):
    return slugify(getattr(model_instance, slugable_field_name))
