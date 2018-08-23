from django.urls import path

from .views import PluginList, PluginNew


urlpatterns = [
    path('', PluginList.as_view(), name='list'),
    path('new/', PluginNew.as_view(), name='new'),
]
