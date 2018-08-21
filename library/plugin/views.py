from django.views.generic import ListView

from .models import Plugin


class PluginList(ListView):
    queryset = Plugin.objects.filter(published=True)
    context_object_name = 'plugins'
