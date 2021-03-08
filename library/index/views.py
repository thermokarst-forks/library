# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.views.generic import ListView, TemplateView
from django.http import HttpResponse

from library.plugins.models import LegacyPlugin
from library.index.tasks import debug


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'plugins'

    def get_queryset(self):
        return LegacyPlugin.objects.sorted_authors(self.request.user).order_by('-created_at')[:6]


class AboutView(TemplateView):
    template_name = 'about.html'


def debug_celery_view(req):
    result = debug.delay(req.GET)
    return HttpResponse('%s\n%s' % (result, result.get(timeout=1)),
                        content_type='text/plain')
