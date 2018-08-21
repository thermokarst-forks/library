from django.db import models

from library.util.models import AuditModel


# TODO: create fixtures for loading "official" plugins
#       https://docs.djangoproject.com/en/2.1/howto/initial-data/
class Plugin(AuditModel):
    name = models.CharField(max_length=500, unique=True)
    short_summary = models.CharField(max_length=500)
    description = models.TextField()
    install_guide = models.TextField()
    draft = models.BooleanField(default=True)
    help_url = models.CharField(max_length=500)

    # TODO: author?

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']
