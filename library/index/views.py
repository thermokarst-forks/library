from django.views.generic import ListView, TemplateView

from library.plugins.models import Plugin


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'plugins'

    def get_queryset(self):
        return Plugin.objects.sorted_authors(self.request.user).order_by('-created_at')[:6]


class AboutView(TemplateView):
    template_name = 'about.html'
