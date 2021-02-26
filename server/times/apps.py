from django.apps import AppConfig


class TimesConfig(AppConfig):
    name = 'times'

    def ready(self):
        from . import signals, models
        from .publish import Publish
        models.publish = Publish()
