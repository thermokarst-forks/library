from django.views.generic import ListView, RedirectView, FormView
from django.urls import reverse_lazy

from django.contrib import admin

from .models import Plugin


class PluginList(ListView):
    queryset = Plugin.objects.filter(published=True)
    context_object_name = 'plugins'


# https://django-authority.readthedocs.io/en/latest/
class PluginNew(FormView):
    template_name = 'admin/change_form.html'

    def get_form(self, form_class=None):
        print(dir(admin.site._registry[Plugin]))
        return admin.site._registry[Plugin].get_form(self.request)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        return {**kwargs, 'opts': admin.site._registry[Plugin].opts}
