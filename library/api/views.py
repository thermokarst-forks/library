from django import http
from django.views.decorators import csrf

from . import forms
from . import tasks
from ..plugins.models import Plugin


@csrf.csrf_exempt
def prepare_packages_for_integration(request):
    if request.method != 'POST':
        payload = {'status': 'error',
                   'errors': {'http_method': 'invalid http method'}}
        return http.JsonResponse(payload, status=405)

    form = forms.PackageIntegrationForm(request.POST)

    if not form.is_valid():
        payload = {'status': 'error', 'errors': form.errors}
        return http.JsonResponse(payload, status=400)

    # Look up UUID, make sure its valid before submitting to celery
    try:
        Plugin.unsafe.get(token=form.cleaned_data['token'])
    except Plugin.DoesNotExist:
        payload = {'status': 'error', 'errors': {'uuid': 'plugin does not exist'}}
        return http.JsonResponse(payload, status=400)

    # Okay, if we made it this far, then we are ready to start the real work
    tasks.fetch_package_from_github.delay(form.cleaned_data)

    payload = {'status': 'ok'}
    return http.JsonResponse(payload, status=200)
