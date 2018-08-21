from django.urls import path

from .views import PluginList


urlpatterns = [
    path('', PluginList.as_view(), name='list'),
]
