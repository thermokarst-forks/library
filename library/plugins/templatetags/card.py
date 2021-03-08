# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from . import register


@register.inclusion_tag('plugins/_card.html')
def card(plugin, is_detail=False):
    return {'plugin': plugin, 'is_detail': is_detail}
