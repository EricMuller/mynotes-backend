
from .permissions import EverybodyCanAuthentication
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from .providers.linkedin_oauth2.views import LinkedInOAuth2Adapter


from rest_auth.registration.views import SocialLoginView

# from rest_framework.response import Response


def confirm_email(self, request, email_address):
    """
    Marks the email address as confirmed on the db
    """
    email_address.verified = True
    email_address.set_as_primary(conditional=True)
    email_address.save()

    return Response({'token': 'OK'})


class Login(APIView):
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

        # return Response({'token': token.key, 'username': user.username, })

        return Response(status=200, data={
            'key': token.key
        })


login_view = Login.as_view()
# Check the credentials and return the REST Token


class GoogleLogin(SocialLoginView):
    """
    Check the Gogle OAuth2 access_token and return the REST Token
    """
    adapter_class = GoogleOAuth2Adapter 


class LinkedInOAuth2Login(SocialLoginView):
    """
    Check the LinkedIn OAuth2 access_token and return the REST Token
    """
    adapter_class = LinkedInOAuth2Adapter


login_google_view = GoogleLogin.as_view()
login_linkedin_view = LinkedInOAuth2Login.as_view()
