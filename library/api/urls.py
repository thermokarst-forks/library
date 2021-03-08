# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.urls import path, include

from . import views


app_name = 'api'


urlpatterns = [
    path('packages/', include([
        path('integrate/', views.prepare_packages_for_integration, name='package-integrate')
    ]))
]
