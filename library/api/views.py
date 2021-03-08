# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django import http
from django.views.decorators import csrf

from . import forms
from . import tasks


@csrf.csrf_exempt
def prepare_packages_for_integration(request):
    if request.method != 'POST':
        payload = {'status': 'error', 'errors': {'http_method': 'invalid http method'}}
        return http.JsonResponse(payload, status=405)

    form = forms.PackageIntegrationForm(request.POST)

    # First line of checks: ensure that the payload is well formed
    if not form.is_valid():
        payload = {'status': 'error', 'errors': form.errors}
        return http.JsonResponse(payload, status=400)

    # Next, we actually check if we know about this plugin, without leaking that info to the requester
    if (config := form.is_known()):
        tasks.handle_new_builds(config)

    payload = {'status': 'ok'}
    return http.JsonResponse(payload, status=200)
