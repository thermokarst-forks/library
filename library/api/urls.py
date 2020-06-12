from django.urls import path, include

from . import views


app_name = 'api'


urlpatterns = [
    path('packages/', include([
        path('integrate/', views.prepare_packages_for_integration, name='package-integrate')
    ]))
]
