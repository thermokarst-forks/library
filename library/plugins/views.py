from django.views.generic import ListView, RedirectView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin

from library.utils.views import SlugPKDetailView
from .models import Plugin


class PluginList(ListView):
    queryset = Plugin.including.sorted_authors().filter(published=True)
    context_object_name = 'plugins'


# TODO: make this a real view, instead of an admin redirect
class PluginNew(RedirectView):
    pattern_name = 'admin:plugins_plugin_add'


class PluginAuthMixin(UserPassesTestMixin):
    login_url = 'foo'

    def test_func(self):
        plugin = self.get_object()
        if plugin.published:
            return True
        return self.request.user in plugin.authors.all()


class PluginDetail(PluginAuthMixin, SlugPKDetailView):
    queryset = Plugin.including.sorted_authors()
    context_object_name = 'plugin'
