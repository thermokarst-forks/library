from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from library.utils.models import AuditModel


User = get_user_model()


class PluginIncludingXQuerySet(models.QuerySet):
    def sorted_authors(self):
        return self.prefetch_related(
            models.Prefetch(
                'authors',
                queryset=User.objects.order_by('plugin_author_list__list_position'),
            )
        )


class Plugin(AuditModel):
    name = models.CharField(max_length=500, unique=True)
    short_summary = models.CharField(max_length=500)
    description = models.TextField()
    install_guide = models.TextField()
    published = models.BooleanField(default=False)

    # TODO: version/release

    authors = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     # use a bridge table with ordering info
                                     through='PluginAuthorship',
                                     related_name='plugins')

    including = PluginIncludingXQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']


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
