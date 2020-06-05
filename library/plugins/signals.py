from django.db.models.signals import pre_save
from django.dispatch import receiver

from library.utils import slug
from .models import LegacyPlugin


@receiver(pre_save, sender=LegacyPlugin)
def slug_handler(sender, instance, **kwargs):
    instance.slug = slug(instance, 'title', 'slug')
