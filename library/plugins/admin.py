from django.contrib import admin

from .models import Plugin, PluginAuthorship


class AuthorInline(admin.TabularInline):
    model = Plugin.authors.through
    extra = 1


class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'published', 'short_summary')
    inlines = [AuthorInline]


class PluginAuthorshipAdmin(admin.ModelAdmin):
    list_display = ('plugin', 'author', 'list_position')


admin.site.register(Plugin, PluginAdmin)
admin.site.register(PluginAuthorship, PluginAuthorshipAdmin)
