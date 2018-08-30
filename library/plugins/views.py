from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect

from .models import Plugin
from .forms import PluginForm


class RedirectSlugMixin:
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        if self.kwargs.get(self.pk_url_kwarg) is None:
            return HttpResponseRedirect(self.object.get_absolute_url())
        return resp


class PluginList(ListView):
    context_object_name = 'plugins'

    def get_queryset(self):
        return Plugin.objects.sorted_authors(self.request.user).order_by('title')


class PluginDetail(RedirectSlugMixin, DetailView):
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


class PluginEdit(LoginRequiredMixin, RedirectSlugMixin, UpdateView):
    context_object_name = 'plugin'
    form_class = PluginForm

    def get_queryset(self):
        return Plugin.objects.sorted_authors(self.request.user)
