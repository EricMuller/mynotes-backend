from rest_framework import parsers
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView

from rest_framework.response import Response

from rest_framework.views import APIView
from webmarks.authentication.permissions import EverybodyCanAuthentication
from webmarks.bookmarks import models
from webmarks.base.models import Folder
from webmarks.bookmarks.serializers import IdSerializer


class SeachNoteView(APIView):
    throttle_classes = ()
    permission_classes = (EverybodyCanAuthentication)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token})


class AddFoldertoBookmark(CreateAPIView, DestroyAPIView):
    """
    post:
        Add folder to Bookmark.

    delete:
        Remove folder to Bookmark.

    """
    querySet = models.Bookmark.objects.all()
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = IdSerializer

    def delete(self, request, pk, id, *args, **kwargs):

        bookmark = models.Bookmark.objects.get(pk=pk)
        folder = Folder.objects.get(pk=id)

        bookmark.folders.remove(folder)
        bookmark.save()

        return Response({'result': 'OK'})

    def post(self, request, pk, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        folderId = serializer.validated_data['id']

        bookmark = models.Bookmark.objects.get(pk=pk)
        folder = Folder.objects.get(pk=folderId)

        bookmark.folders.add(folder)
        bookmark.save()

        return Response(serializer.data)


add_folder_bookmark_view = AddFoldertoBookmark.as_view()
