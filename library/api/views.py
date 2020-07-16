from django import http, conf
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

        Plugin.unsafe.get(token=form.cleaned_data['qiime2_plugin_token'])
    except Plugin.DoesNotExist:
        payload = {'status': 'error', 'errors': {'uuid': 'plugin does not exist'}}
        return http.JsonResponse(payload, status=400)

    # Okay, if we made it this far, then we are ready to start the real work
    tasks.handle_new_builds({
        'plugin_name': form.cleaned_data['plugin_name'],
        'repository': form.cleaned_data['repository'],
        'run_id': form.cleaned_data['run_id'],
        'github_token': conf.settings.GITHUB_TOKEN,
        'conda_asset_path': conf.settings.CONDA_ASSET_PATH,
    })

    payload = {'status': 'ok'}
    return http.JsonResponse(payload, status=200)
