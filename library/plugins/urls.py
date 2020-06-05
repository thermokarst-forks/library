from django.urls import path, include

from .views import LegacyPluginList, LegacyPluginNew, LegacyPluginDetail, LegacyPluginEdit


urlpatterns = [
    path('', LegacyPluginList.as_view(), name='list'),
    path('new/', LegacyPluginNew.as_view(), name='new'),
    path('<slug:slug>/', include([
        path('', LegacyPluginDetail.as_view(), name='detail_slug'),
        path('<int:pk>/', include([
            path('', LegacyPluginDetail.as_view(), name='detail_pk'),
            path('edit/', LegacyPluginEdit.as_view(), name='edit')
        ]))
    ]))
]
