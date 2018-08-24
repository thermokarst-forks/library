from django.db import models

from library.utils.models import AuditModel
from library.users.models import User


class Plugin(AuditModel):
    name = models.CharField(max_length=500, unique=True)
    short_summary = models.CharField(max_length=500)
    description = models.TextField()
    install_guide = models.TextField()
    published = models.BooleanField(default=False)

    # TODO: version/release

    authors = models.ManyToManyField(User, through='PluginAuthorship',
                                     related_name='plugins')

    def get_authors(self):
        return self.authors.order_by('list_position')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']


class PluginAuthorship(AuditModel):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE,
                               related_name='+')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='+')
    list_position = models.IntegerField(
        help_text='This field will specify the sort order the plugin authors '
                  'will be displayed in.')

    def __str__(self):
        return '%s - %s (%d)' % (self.plugin, self.author, self.list_position)

    class Meta:
        verbose_name_plural = 'plugin authorship'
        unique_together = (('plugin', 'author'), )
