from django.apps import AppConfig


class CircleConfig(AppConfig):
    name = 'circle'

    def ready(self):
        from . import signals
