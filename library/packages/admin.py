from django.contrib import admin

from .models import Package, PackageBuild


class PackageBuildInline(admin.TabularInline):
    model = PackageBuild
    readonly_fields = ('package', 'github_run_id', 'version')
    extra = 0
    can_delete = False


class PackageAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'repository', 'token')
    inlines = [PackageBuildInline]


class PackageBuildAdmin(admin.ModelAdmin):
    readonly_fields = ('package', 'github_run_id', 'version')


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageBuild, PackageBuildAdmin)
