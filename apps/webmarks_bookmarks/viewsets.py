from webmarks_django_contrib.cache import CustomListKeyConstructor
from webmarks_django_contrib.viewsets import AggregateModelViewSet
from webmarks_crawler.crawler import Crawler
from webmarks_bookmarks import models
from webmarks_bookmarks import serializers
from webmarks_bookmarks.filters import BookmarkFilter
from webmarks_bookmarks.filters import TagFilter
from webmarks_folders.filters import FolderFilter
from webmarks_folders.models import Folder
from webmarks_folders.serializers import FolderSerializer
from webmarks_storage.storages import FileStore
from rest_framework import filters
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework import permissions
import base64
import logging

from webmarks_storage.models import DataStorage
from webmarks_storage.models import Store
from webmarks_storage.serializers import DataStorageSerializer

stdlogger = logging.getLogger(__name__)


class FolderViewSet(AggregateModelViewSet):
    """
    retrieve:
        Return a Folder instance.

    list:
        Return all Folder instance , ordered by most recently created.

    create:
        Create a new Folder.

    delete:
        Remove an existing Folder.

    partial_update:
        Update one or more fields on an existing Folder.

    update:
        Update a Folder.
    """
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = FolderFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):

        return Folder.objects.filter(user_cre_id=self.request.user.id)

    @detail_route(methods=['get'])
    def bookmarks(self, request, pk):
        """
            Return all bookmarks of folder.
        """
        self.queryset = models.Bookmark.objects.filter(folders__in=[pk])

        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = serializers.BookmarkSerializer(
                self.queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.BookmarkSerializer(self.queryset, many=True)
        return Response(serializer.data)


class BookmarkViewSet(AggregateModelViewSet):

    """
    retrieve:
        Return a Bookmark instance.

    list:
        Return all Bookmark instance , ordered by most recently created.

    create:
        Create a new Bookmark.

    delete:
        Remove an existing Bookmark.

    partial_update:
        Update one or more fields on an existing Bookmark.

    update:
        Update a Bookmark.
    """

    queryset = models.Bookmark.objects.prefetch_related('tags')
    serializer_class = serializers.BookmarkSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = BookmarkFilter
    permission_classes = (permissions.IsAuthenticated,)

    @cache_response(key_func=CustomListKeyConstructor())
    def list(self, *args, **kwargs):
        return super(BookmarkViewSet, self).list(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        # print('user_id=' + str(self.request.user.id))
        return models.Bookmark.objects.prefetch_related('tags').filter(
            user_cre_id=self.request.user.id)

    def get_serializer_class(self):
        # if self.action == 'list':
        #    return serializers.NoteListSerializer
        return serializers.BookmarkSerializer

    @detail_route(methods=['get'])
    def title(self, request, pk=None):
        """
            Return the title of url's Page Bookmark.
        """
        crawler = Crawler()
        stdlogger.debug(pk)
        url = base64.b64decode(pk)
        stdlogger.info(url.decode())
        crawler.crawl_title(url.decode())
        serializer = serializers.CrawlSerializer(crawler)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def store(self, request, pk):
        """
            Crawl and Archive the Url Bookmark Page.
        """
        bookmark = self.get_object()
        stdlogger.debug(pk)
        crawler = Crawler()
        # url = base64.b64decode(pk)
        # stdlogger.info(url.decode())
        crawler.crawl(bookmark.url)
        # indexes = {"title": bookmark.title, "url": bookmark}
        try:
            store = Store.objects.filter(
                user_uuid=request.user.uuid).get(kind=Store.WBM_STORE)
        except Store.DoesNotExist:
            store = Store.create(Store.WBM_STORE, request.user.uuid)
            store.save()

        archive = DataStorage.create(
            bookmark.uuid, crawler.content_type, store)
        archive.save()

        indexes = self.serializer_class(bookmark).data
        FileStore().store(str(archive.id), request.user.username,
                          crawler.html.encode(), indexes)

        bookmark.archive_id = archive.id
        bookmark.save()
        serializer = DataStorageSerializer(archive)
        return Response(serializer.data)


class TagViewSet(AggregateModelViewSet):
    """
    retrieve:
        Return a Tag instance.

    list:
        Return all Tag instance , ordered by most recently created.

    create:
        Create a new Tag.

    delete:
        Remove an existing Tag.

    partial_update:
        Update one or more fields on an existing Tag.

    update:
        Update a Tag.
    """
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TagFilter
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(methods=['get'])
    def count(self, request):
        queryset = models.Tag.objects.with_counts(user_cre_id=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.TagCountSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer = serializers.TagCountSerializer(queryset, many=True)
        return Response(serializer.data)
