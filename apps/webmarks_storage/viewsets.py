from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from webmarks_django_contrib.paginators import SpringSetPagination

from webmarks_storage import models
from webmarks_storage import serializers
from webmarks_storage.storages import FileStore


class FileStorageViewSet(viewsets.ModelViewSet):
    parser_classes = (FileUploadParser)
    permission_classes = (permissions.IsAuthenticated,)
    # overriding default query set


class StoreViewSet(ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer

    permission_classes = (permissions.AllowAny,)
    pagination_class = SpringSetPagination


class DataStorageViewSet(ModelViewSet):
    """
    retrieve:
        Return a Archive instance.

    list:
        Return all Archives, ordered by most recently joined.

    create:
        Create a new Archive.

    delete:
        Remove an existing Archive.

    partial_update:
        Update one or more fields on an existing Archive.

    update:
        Update a Archive.
    """

    filter_backends = (filters.DjangoFilterBackend,)
    queryset = models.DataStorage.objects.all()
    serializer_class = serializers.DataStorageSerializer

    permission_classes = (permissions.AllowAny,)
    pagination_class = SpringSetPagination

    def retrieve(self, request, pk, format=None):
        archive = get_object_or_404(models.DataStorage, pk=pk)
        if request.accepted_renderer.format == 'html':
            return Response(archive.data)

        serializer = self.serializer_class(archive)
        response = Response(serializer.data)
        response['Cache-Control'] = 'no-cache'
        return response

    @detail_route(methods=['get'])
    def download(self, request, pk):
        """
            Download Archive File.
        """
        archive = get_object_or_404(models.DataStorage, pk=pk)

        archive_name = FileStore().get_file_path(str(archive.id),
                                                 request.user.username)

        return FileResponse(open(archive_name, 'rb'))
