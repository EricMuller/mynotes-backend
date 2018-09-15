from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'webmarks_users'
    verbose_name = 'Users'
    label = 'webmarks_users'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
