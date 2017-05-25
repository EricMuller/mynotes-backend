from django.apps import AppConfig


class BookmarksConfig(AppConfig):
    name = 'webmarks.bookmarks'
    label = 'bookmarks'

    def ready(self):
        import webmarks.bookmarks.signals.handlers  # noqa
