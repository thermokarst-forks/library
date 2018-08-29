from django.views.generic import ListView, RedirectView
from django.db import models

from library.utils.views import SlugPKDetailView, SlugPKUpdateView
from .models import Plugin


class PluginList(ListView):
    context_object_name = 'plugins'

    def get_queryset(self):
        qs = Plugin.objects.sorted_authors(self.request.user) | Plugin.unsafe.filter(published=True)
        return qs.distinct()


# TODO: make this a real view, instead of an admin redirect
class PluginNew(RedirectView):
    pattern_name = 'admin:plugins_plugin_add'


class PluginDetail(SlugPKDetailView):
    context_object_name = 'plugin'

    def get_queryset(self):
        qs = Plugin.objects.all(self.request.user) | Plugin.unsafe.filter(published=True)
        return qs.distinct()


class PluginEdit(SlugPKUpdateView):
    context_object_name = 'plugin'
    fields = ['name']

    def get_queryset(self):
        return Plugin.objects.all(self.request.user)
