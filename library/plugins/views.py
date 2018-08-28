from django.views.generic import ListView, RedirectView

from library.utils.views import SlugPKDetailView
from .models import Plugin


class PluginList(ListView):
    queryset = Plugin.including.sorted_authors().filter(published=True)
    context_object_name = 'plugins'


# TODO: make this a real view, instead of an admin redirect
class PluginNew(RedirectView):
    pattern_name = 'admin:plugins_plugin_add'


class PluginDetail(SlugPKDetailView):
    queryset = Plugin.including.sorted_authors()
    context_object_name = 'plugin'
