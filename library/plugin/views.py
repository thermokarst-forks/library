from django.views.generic import TemplateView


class ListView(TemplateView):
    template_name = 'plugin/list.html'
