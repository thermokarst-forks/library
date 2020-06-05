from django.contrib import admin

from .models import Plugin, LegacyPlugin, LegacyPluginAuthorship


class LegacyAuthorInline(admin.TabularInline):
    model = LegacyPlugin.authors.through
    extra = 1


class LegacyPluginAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'short_summary')
    readonly_fields = ('slug',)
    inlines = [LegacyAuthorInline]


class LegacyPluginAuthorshipAdmin(admin.ModelAdmin):
    list_display = ('plugin', 'author', 'list_position')


class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'token')
    readonly_fields = ('token', )


admin.site.register(LegacyPlugin, LegacyPluginAdmin)
admin.site.register(LegacyPluginAuthorship, LegacyPluginAuthorshipAdmin)
admin.site.register(Plugin, PluginAdmin)
