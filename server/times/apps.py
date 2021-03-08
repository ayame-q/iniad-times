from django.apps import AppConfig


class TimesConfig(AppConfig):
    name = 'times'

    def ready(self):
        from . import signals, models, publish
        import sys
        if not "manage.py" in sys.argv or "runserver" in sys.argv:
            models.publish = publish.Publish()
