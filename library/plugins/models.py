from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from library.utils.models import AuditModel


User = get_user_model()


# Global Workgroup Access Restriction
class GWARManager(models.Manager):
    def get_queryset(self, user):
        qs = super().get_queryset()
        # If current user is a `superuser` let them go wherever they want!
        # With great power comes great responsibility.
        if user.is_superuser:
            return qs
        # Can't filter on an AnonymousUser, so, we just limit to `published`,
        # since they can't be an author, anyway.
        if user.is_anonymous:
            return qs.filter(published=True)
        # Finally, for a regular, logged in user, only show them `published`
        # plugins, unless they are an author on an unpublished plugin.
        return qs.filter(models.Q(authors=user) | models.Q(published=True))

    def all(self, user):
        return self.get_queryset(user)

    def sorted_authors(self, user):
        return self.get_queryset(user).prefetch_related(
            models.Prefetch(
                'authors',
                queryset=User.objects.order_by('plugin_author_list__list_position'),
            )
        )


_help_text = {
    'name': 'The plugin\'s name, as registered in QIIME 2. (e.g. my_plugin).',
    'title': 'The plugin\'s project title (e.g. q2-my-plugin).',
    'short_summary': 'This field is displayed in "overviews" such as the plugin listing page.',
    'description': 'A free-form description of the plugin.',
    'install_guide': 'This field should contain directions (or a link to directions) on how to install the plugin.',
    'published': 'This field controls the plugin\'s visibility to other users on library.qiime2.org.  Only mark as '
                 '"true" if you are prepared for the plugin to go "live"!',
    'source_url': 'The URL for obtaining the plugin\'s source code.',
    'version': 'The current version of the plugin.',
}


class Plugin(AuditModel):
    name = models.CharField(max_length=500, unique=True, help_text=_help_text['name'])
    title = models.CharField(max_length=500, unique=True, help_text=_help_text['title'])
    slug = models.SlugField(max_length=500, unique=True)
    short_summary = models.CharField(max_length=500, help_text=_help_text['short_summary'])
    description = models.TextField(help_text=_help_text['description'])
    install_guide = models.TextField(help_text=_help_text['install_guide'])
    published = models.BooleanField(default=False, help_text=_help_text['published'])
    source_url = models.URLField(max_length=500, blank=True, help_text=_help_text['source_url'])
    version = models.CharField(max_length=500, blank=True, help_text=_help_text['version'])

    # RELATIONSHIPS
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     # use a bridge table with ordering info
                                     through='PluginAuthorship',
                                     related_name='plugins')
    # For now, no reverse relationships. Also, no order on relationships.
    dependencies = models.ManyToManyField('self', symmetrical=False, db_table='plugins_plugin_dependencies')

    # MANAGERS
    objects = GWARManager()
    unsafe = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:detail_pk', args=[self.slug, str(self.id)])

    class Meta:
        ordering = ['-updated_at']
        # This is so that the `admin` app still works as expected
        default_manager_name = 'unsafe'


class PluginAuthorship(AuditModel):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE,
                               related_name='plugin_author_list')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='plugin_author_list')
    list_position = models.IntegerField(
        help_text='This field will specify the sort order the plugin authors '
                  'will be displayed in.')

    def __str__(self):
        return '%s - %s (%d)' % (self.plugin, self.author, self.list_position)

    class Meta:
        verbose_name_plural = 'plugin authorship'
        # Can't be listed as an author more than once for any given plugin
        unique_together = (('plugin', 'author'), )
