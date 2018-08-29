from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['authors'] = self.object.authors.all()
        ctx['current_user_is_author'] = user in ctx['authors'] or user.is_superuser
        return ctx


class PluginNew(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    context_object_name = 'plugin'
    permission_required = 'forum_trust_level_1'
    model = Plugin
    form_class = PluginForm


class PluginEdit(LoginRequiredMixin, SlugPKUpdateView):
    context_object_name = 'plugin'
    form_class = PluginForm

    def get_queryset(self):
        return Plugin.objects.sorted_authors(self.request.user)
