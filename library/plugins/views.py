from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect

from .models import Plugin
from .forms import PluginForm, PluginAuthorshipFormSet


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


# https://stackoverflow.com/a/11910420/313548
class PluginNew(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    context_object_name = 'plugin'
    permission_required = 'forum_trust_level_1'
    model = Plugin
    form_class = PluginForm

    def get_named_formsets(self):
        return {
            'plugin_author': PluginAuthorshipFormSet(self.request.POST or None, prefix='plugin_author'),
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()

        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        print('neat')
        self.object = form.save()
        # resp = self.form_valid(form)

        for name, formset in named_formsets.items():
            print(name)
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        print('why')
        return resp


class PluginEdit(LoginRequiredMixin, RedirectSlugMixin, UpdateView):
    context_object_name = 'plugin'
    form_class = PluginForm

    def get_queryset(self):
        return Plugin.objects.sorted_authors(self.request.user)
