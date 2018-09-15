from django.apps import AppConfig


class BookmarksConfig(AppConfig):
    name = 'webmarks_bookmarks'
    label = 'webmarks_bookmarks'

    def ready(self):
        import webmarks_bookmarks.signals.handlers  # noqa
