from django.apps import AppConfig


class BookmarksConfig(AppConfig):
    name = 'webmarks.bookmarks'
    label = 'webmarks_bookmarks'

    def ready(self):
        import webmarks.bookmarks.signals.handlers  # noqa
