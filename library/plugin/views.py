from django.views.generic import ListView

from .models import Plugin


class PluginList(ListView):
    queryset = Plugin.objects.filter(draft=False)
