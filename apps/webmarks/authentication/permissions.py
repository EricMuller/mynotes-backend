
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


class DefaultsAuthentificationMixin(object):
    """Default settings for view authentication, permissions,
    filtering and pagination."""

    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
    )

    permission_classes = (permissions.IsAuthenticated,)


class EverybodyCanAuthentication(SessionAuthentication):
    def authenticate(self, request):
        return None
