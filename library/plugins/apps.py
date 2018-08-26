from django.apps import AppConfig


class PluginConfig(AppConfig):
    name = 'library.plugins'

    def ready(self):
        # register the decorated signals
        from . import signals  # noqa: F401
