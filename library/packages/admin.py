# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.contrib import admin

from .models import Package, PackageBuild


class PackageBuildInline(admin.TabularInline):
    model = PackageBuild
    readonly_fields = ('package', 'github_run_id', 'version', 'linux_64', 'osx_64',
                       'integration_pr_url', 'release')
    extra = 0
    can_delete = False

    def has_add_permission(self, req, obj):
        return False


class PackageAdmin(admin.ModelAdmin):
    readonly_fields = ('token', )
    inlines = [PackageBuildInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('name', 'repository')
        else:
            return self.readonly_fields


class PackageBuildAdmin(admin.ModelAdmin):
    readonly_fields = ('package', 'github_run_id', 'version', 'linux_64', 'osx_64',
                       'integration_pr_url', 'release')


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageBuild, PackageBuildAdmin)
