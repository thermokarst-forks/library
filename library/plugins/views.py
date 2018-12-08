from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect

from .models import Plugin, PluginAuthorship
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


class PluginNew(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    context_object_name = 'plugin'
    permission_required = 'plugins.add_plugin'
    model = Plugin
    form_class = PluginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = None
        ctx = self.get_context_data(form=self.get_form(),
                                    author_formset=PluginAuthorshipFormSet(user=self.request.user))
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        author_formset = PluginAuthorshipFormSet(self.request.POST, user=self.request.user)
        form_is_valid = form.is_valid()
        author_formset_is_valid = author_formset.is_valid()
        if form_is_valid and author_formset_is_valid:
            return self.form_valid(form, author_formset)
        else:
            return self.form_invalid(form, author_formset)

    def form_valid(self, form, author_formset):
        self.object = form.save()
        author_forms = author_formset.save(commit=False)
        for author_form in author_forms:
            author_form.plugin = self.object
            author_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, author_formset):
        ctx = self.get_context_data(form=form, author_formset=author_formset)
        return self.render_to_response(ctx)


class PluginEdit(LoginRequiredMixin, RedirectSlugMixin, UpdateView):
    context_object_name = 'plugin'
    form_class = PluginForm

    def get_queryset(self):
        user = self.request.user
        qs = Plugin.objects.all(user)
        if user.is_superuser:
            return qs
        return qs.filter(authors__in=[user])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        qs = PluginAuthorship.objects.all().order_by('list_position')
        ctx = self.get_context_data(
            form=self.get_form(),
            author_formset=PluginAuthorshipFormSet(instance=self.object,
                                                   queryset=qs, user=self.request.user))
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        author_formset = PluginAuthorshipFormSet(self.request.POST, instance=self.object, user=self.request.user)
        form_is_valid = form.is_valid()
        author_formset_is_valid = author_formset.is_valid()
        if form_is_valid and author_formset_is_valid:
            return self.form_valid(form, author_formset)
        else:
            return self.form_invalid(form, author_formset)

    def form_valid(self, form, author_formset):
        self.object = form.save()
        author_forms = author_formset.save(commit=False)
        for author_form in author_forms:
            author_form.plugin = self.object
            author_form.save()
        for author in author_formset.deleted_objects:
            author.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, author_formset):
        ctx = self.get_context_data(form=form, author_formset=author_formset)
        return self.render_to_response(ctx)
