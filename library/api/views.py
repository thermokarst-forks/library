from .forms import PackageIntegrationForm


def prepare_packages_for_integration(request):
    if request.method != 'POST':
        return HttpResponse('Invalid method', status=405)

    # do something with the form
