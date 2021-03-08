# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from . import register


@register.inclusion_tag('utils/_form_field.html')
def form_field(field, outer_class='control'):
    return {'field': field, 'outer_class': outer_class}
