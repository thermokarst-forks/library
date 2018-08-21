from django.contrib import admin
from django.urls import path, include

from library.util import views as util_views


urlpatterns = [
    path('', util_views.ListView.as_view(), name='index'),
    path('plugins/', include(('library.plugin.urls', 'plugin'),
                             namespace='plugin')),
    path('admin/', admin.site.urls),
]
