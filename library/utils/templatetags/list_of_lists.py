# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from . import register


@register.filter(name='list_of_lists')
def list_of_lists(value, n):
    for i in range(0, len(value), n):
        yield value[i:i + n]
