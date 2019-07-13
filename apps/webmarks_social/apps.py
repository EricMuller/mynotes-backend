from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'webmarks_social'
    verbose_name = 'Users'
    label = 'webmarks_social'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
