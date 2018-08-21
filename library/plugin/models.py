from django.db import models

from library.util.models import AuditModel


# Fixtures script:
#     https://gist.github.com/thermokarst/7c7e3796ec4b0577c1e53a93181f960b
class Plugin(AuditModel):
    name = models.CharField(max_length=500, unique=True)
    short_summary = models.CharField(max_length=500)
    description = models.TextField()
    install_guide = models.TextField()
    published = models.BooleanField(default=False)

    # TODO: author
    # TODO: version/release

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']
