from django.apps import AppConfig


class TimesConfig(AppConfig):
    name = 'times'

    def ready(self):
        from . import signals
