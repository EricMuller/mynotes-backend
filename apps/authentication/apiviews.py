from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login

from .permissions import EverybodyCanAuthentication
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
# from rest_framework.response import Response


def confirm_email(self, request, email_address):
    """
    Marks the email address as confirmed on the db
    """
    email_address.verified = True
    email_address.set_as_primary(conditional=True)
    email_address.save()

    return Response({'token': 'OK'})


class ObtainAuthToken(APIView):
    throttle_classes = ()
    # permission_classes = (EverybodyCanAuthentication,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    authentication_classes = (EverybodyCanAuthentication,)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'username': user.username, })


obtain_auth_token = ObtainAuthToken.as_view()


# Add a user to the system based on facebook token
class FacebookLoginOrSignup(APIView):

    permission_classes = (AllowAny,)

    # this is a public api!!!
    authentication_classes = (EverybodyCanAuthentication,)

    serializer_class = AuthTokenSerializer

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
