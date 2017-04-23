from django.apps import AppConfig


class MynotesConfig(AppConfig):
    name = 'apps.mynotes'
    label = 'mynotes'

    def ready(self):
        import apps.mynotes.signals.handlers  # noqa
