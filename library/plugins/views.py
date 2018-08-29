from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from library.utils.views import SlugPKDetailView, SlugPKUpdateView
from .models import Plugin
from .forms import PluginForm


class PluginList(ListView):
    context_object_name = 'plugins'

    def get_queryset(self):
        return Plugin.objects.sorted_authors(self.request.user)


class PluginDetail(SlugPKDetailView):
    context_object_name = 'plugin'

    def get_queryset(self):
        return Plugin.objects.sorted_authors(self.request.user)


class PluginNew(LoginRequiredMixin, CreateView):
    context_object_name = 'plugin'
    model = Plugin
    form_class = PluginForm


class PluginEdit(LoginRequiredMixin, SlugPKUpdateView):
    context_object_name = 'plugin'
    form_class = PluginForm

    def get_queryset(self):
        return Plugin.objects.sorted_authors(self.request.user)
