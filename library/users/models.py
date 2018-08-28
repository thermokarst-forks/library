import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from library.utils.models import AuditModel


# There are several unused cols in the database, but it is a lot easier to just
# accept that vs define models that fit the auth.User API:
# https://docs.djangoproject.com/en/2.1/topics/auth/
#     customizing/#specifying-custom-user-model
class User(AbstractUser, AuditModel):
    full_name = models.CharField(blank=True, max_length=300)
    forum_external_id = models.CharField(max_length=100, unique=True,
            blank=False, default=uuid.uuid4)
    forum_avatar_url = models.URLField(blank=True)
    forum_is_admin = models.BooleanField(default=False)
    forum_is_moderator = models.BooleanField(default=False)

    def get_full_name(self):
        return self.full_name.strip()

    def get_short_name(self):
        return self.full_name.strip()

    def get_absolute_url(self):
        return 'https://forum.qiime2.org/u/%s' % self.username
