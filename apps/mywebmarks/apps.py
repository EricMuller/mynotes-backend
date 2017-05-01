from django.apps import AppConfig


class MyWebmarksConfig(AppConfig):
    name = 'apps.mywebmarks'
    label = 'mywebmarks'

    def ready(self):
        import apps.mywebmarks.signals.handlers  # noqa
