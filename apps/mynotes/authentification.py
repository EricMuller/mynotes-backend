
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login


class DefaultsAuthentificationMixin(object):
    """Default settings for view authentication, permissions,
    filtering and pagination."""

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,

    )
    permission_classes = (
        permissions.IsAuthenticated,
    )


class EverybodyCanAuthentication(SessionAuthentication):
    def authenticate(self, request):
        return None

# Add a user to the system based on facebook token


class FacebookLoginOrSignup(APIView):

    permission_classes = (AllowAny,)

    # this is a public api!!!
    authentication_classes = (EverybodyCanAuthentication,)

    def dispatch(self, *args, **kwargs):
        return super(FacebookLoginOrSignup, self).dispatch(*args, **kwargs)

    def post(self, request):
        data = JSONParser().parse(request)
        access_token = data.get('access_token', '')

        try:
            app = SocialApp.objects.get(provider="facebook")
            token = SocialToken(app=app, token=access_token)

            # check token against facebook
            login = fb_complete_login(app, token)
            login.token = token
            login.state = SocialLogin.state_from_request(request)

            # add or update the user into users table
            ret = complete_social_login(request, login)

            # if we get here we've succeeded
            return Response(status=200, data={
                'success': True,
                'username': request.user.username,
                'user_id': request.user.pk,
            })

        except:

            return Response(status=401, data={
                'success': False,
                'reason': "Bad Access Token",
            })
