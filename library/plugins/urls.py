from django.urls import path, include

from .views import PluginList, PluginNew, PluginDetail, PluginEdit


urlpatterns = [
    path('', PluginList.as_view(), name='list'),
    path('new/', PluginNew.as_view(), name='new'),
    path('<slug:slug>/', include([
        path('', PluginDetail.as_view(), name='detail_slug'),
        path('<int:pk>/', include([
            path('', PluginDetail.as_view(), name='detail_pk'),
            path('edit/', PluginEdit.as_view(), name='edit')
        ]))
    ]))
]
