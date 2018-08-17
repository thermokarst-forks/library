from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include(('library.search.urls', 'search'), namespace='search')),
    path('admin/', admin.site.urls),
]
