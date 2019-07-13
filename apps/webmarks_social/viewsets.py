from rest_framework.viewsets import ReadOnlyModelViewSet

from webmarks_django_contrib.paginators import SpringSetPagination
from rest_framework import permissions
from webmarks_social.models import User
from webmarks_social.serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = SpringSetPagination

    def get_object(self, request, pk, format=None):
        return self.request.user

    # def list(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)
