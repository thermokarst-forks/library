from django.views.generic import ListView, RedirectView

from .models import Plugin


class PluginList(ListView):
    queryset = Plugin.objects.filter(published=True)
    context_object_name = 'plugins'


# TODO: make this a real view, instead of an admin redirect
class PluginNew(RedirectView):
    pattern_name = 'admin:plugin_plugin_add'
