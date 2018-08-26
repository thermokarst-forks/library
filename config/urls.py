from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from library.utils import views as util_views


urlpatterns = [
    path('', util_views.ListView.as_view(), name='index'),
    path('plugins/', include(('library.plugins.urls', 'plugins'))),
    path('admin/', admin.site.urls),
]


# Debug toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
