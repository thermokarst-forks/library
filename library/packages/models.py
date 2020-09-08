import uuid

from django.db import models


class Package(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    core = models.BooleanField(default=False)
    repository = models.CharField(max_length=255)

    def __str__(self):
        name = self.name if self.name else 'UNSYNCED'
        return 'Package<name=%s, token=%s>' % (name, self.token)


class PackageBuild(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    package = models.ForeignKey('Package', on_delete=models.CASCADE, related_name='package_builds')
    github_run_id = models.CharField(max_length=100)
    version = models.CharField(max_length=255)
    artifact_name = models.CharField(max_length=100)

    def __str__(self):
        return 'PackageBuild<github_run_id=%s, version=%s>' % (self.github_run_id, self.version)
