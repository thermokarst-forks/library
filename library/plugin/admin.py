from django.contrib import admin

from .models import Plugin


class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'draft', 'short_summary', 'help_url')


admin.site.register(Plugin, PluginAdmin)
