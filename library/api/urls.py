from django.urls import path, include

from .views import prepare_package_for_integration


urlpatterns = [
    path('packages/', include([
        path('integrate/', prepare_package_for_integration, name='package-integrate')
    ]))
]
