from django.contrib import admin

from .models import Plugin


class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'published', 'short_summary')


admin.site.register(Plugin, PluginAdmin)
