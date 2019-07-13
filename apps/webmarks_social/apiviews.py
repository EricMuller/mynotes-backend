from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from webmarks_social.serializers import UserSerializer


class ApiCurrentUserView(APIView):
    """
    View curent user

    * Requires token authentication.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return current user.
        """
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)
