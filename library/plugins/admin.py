# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.contrib import admin

from .models import LegacyPlugin, LegacyPluginAuthorship


class LegacyAuthorInline(admin.TabularInline):
    model = LegacyPlugin.authors.through
    extra = 1


class LegacyPluginAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'short_summary')
    readonly_fields = ('slug',)
    inlines = [LegacyAuthorInline]


class LegacyPluginAuthorshipAdmin(admin.ModelAdmin):
    list_display = ('plugin', 'author', 'list_position')


admin.site.register(LegacyPlugin, LegacyPluginAdmin)
admin.site.register(LegacyPluginAuthorship, LegacyPluginAuthorshipAdmin)
