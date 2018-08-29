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


class Plugin(AuditModel):
    name = models.CharField(max_length=500, unique=True, help_text='The plugin\'s name, as registered in QIIME 2.')
    slug = models.SlugField(max_length=500, unique=True)
    title = models.CharField(max_length=500, help_text='The plugin\'s project title (e.g. q2-my-plugin).')
    short_summary = models.CharField(max_length=500)
    description = models.TextField()
    install_guide = models.TextField()
    published = models.BooleanField(default=False)
    source_url = models.URLField(max_length=500, blank=True)
    version = models.CharField(max_length=500, blank=True)

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
