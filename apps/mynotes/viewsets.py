import base64
import logging
import tempfile
from abc import ABCMeta, abstractmethod
from apps.authentication.authentification import DefaultsAuthentificationMixin
from apps.mynotes import models
from apps.mynotes import serializers
from apps.mynotes.crawler import Crawler
from apps.mynotes.filters import NoteFilter
from apps.mynotes.managers import AggregateList
from apps.mynotes.paginators import AggregateResultsViewSetPagination

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import StaticHTMLRenderer


stdlogger = logging.getLogger(__name__)


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class AggregatePaginationReponseMixin(object):

    pagination_class = AggregateResultsViewSetPagination

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None

        if isinstance(self.queryset, AggregateList):
            aggregate_data = self.queryset.aggregate_data
        else:
            aggregate_data = {}

        fields = self.serializer_class.Meta.fields

        return self.paginator.get_paginated_response(self.queryset.model,
                                                     fields,
                                                     data, aggregate_data)


class AggregateModelViewSet(AggregatePaginationReponseMixin,
                            viewsets.ModelViewSet):
    __metaclass__ = ABCMeta

    pass


class NoteViewSet(AggregateModelViewSet, DefaultsAuthentificationMixin):

    queryset = models.Note.objects.prefetch_related('tags')

    # .prefetch_related(
    #    'tags').prefetch_related('archive').values_list('title','rate')
    # queryset = models.Note.objects.prefetch_related('tags').values('archive__note', 'id', 'title', 'url', 'description', 'updated_dt', 'created_dt',
    #    'user_cre', 'user_upd', 'archived_dt', 'rate', 'type', 'status', 'public', 'schedule_dt')

    serializer_class = serializers.NoteSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    # filter_fields = ('id', 'title', 'public', 'description', )
    filter_class = NoteFilter

    def get_queryset(self, *args, **kwargs):
        print('user_id=' + str(self.request.user.id))
        return models.Note.objects.prefetch_related('tags').filter(user_cre_id=self.request.user.id)

    def get_serializer_class(self):

        # if self.action == 'list':
        #    return serializers.NoteListSerializer

        return serializers.NoteSerializer

    @detail_route(methods=['get'])
    def title(self, request, pk=None):
        crawler = Crawler()

        stdlogger.debug(pk)
        url = base64.b64decode(pk)
        stdlogger.info(url.decode())
        crawler.crawl_title(url.decode())
        serializer = serializers.CrawlSerializer(crawler)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def archive(self, request, pk):
        note = self.get_object()
        stdlogger.debug(pk)
        crawler = Crawler()
        # url = base64.b64decode(pk)
        # stdlogger.info(url.decode())
        crawler.crawl(note.url)

        archive = models.Archive.create(
            note, crawler.content_type, crawler.html.encode())

        archive.save()
        note.archive_id = archive.id
        note.save()
        serializer = serializers.ArchiveSerializer(archive)
        return Response(serializer.data)


class TagViewSet(AggregateModelViewSet, DefaultsAuthentificationMixin):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'name', 'public',)


class TagCloudViewSet(AggregatePaginationReponseMixin,
                      viewsets.ReadOnlyModelViewSet):
    """tag with count"""
    queryset = models.Tag.objects.with_counts(-1)
    serializer_class = serializers.TagCloudSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'name', 'public',)

    def get_queryset(self, *args, **kwargs):

        return models.Tag.objects.with_counts(user_cre_id=self.request.user.id)

    @list_route(methods=['get', ])
    def user_tag(self, request, pk=None):

        snippet = pk
        return Response(snippet)


class SearchViewSet(AggregateModelViewSet, DefaultsAuthentificationMixin):
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = models.Search.objects.all()
    serializer_class = serializers.SearchSerializer


class FileUploaderViewSet(DefaultsAuthentificationMixin,
                          viewsets.ModelViewSet):
    serializer_class = serializers.FileUploaderSerializer
    parser_classes = (MultiPartParser, FormParser,)

    # overriding default query set
    queryset = models.FileUploader.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super(FileUploaderViewSet, self).get_queryset(*args, **kwargs)
        qs = qs.filter(owner=self.request.user)
        return qs


class ArchiveViewSet(AggregateModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer,
                        StaticHTMLRenderer,)

    def retrieve(self, request, pk, format=None):
        archive = get_object_or_404(models.Archive, pk=pk)
        if request.accepted_renderer.format == 'html':
            return Response(archive.data)

        serializer = self.serializer_class(archive)
        response = Response(serializer.data)
        response['Cache-Control'] = 'no-cache'
        return response

    @detail_route(methods=['get'])
    def download(self, request, pk):
        archive = get_object_or_404(models.Archive, pk=pk)
        # tmp = tempfile.NamedTemporaryFile(suffix=".note")
        filename = archive.name.split('/')[-1]
        resp = HttpResponse(
            archive.data, content_type='application/text;charset=UTF-8')
        resp['Content-Disposition'] = "attachment; filename=%s" % filename
        return resp


class CrawlerViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):
        crawler = Crawler()
        stdlogger.debug(pk)
        url = base64.b64decode(pk)
        stdlogger.info(url.decode())
        data = crawler.crawl(url.decode())
        serializer = serializers.CrawlSerializer(data)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def title(self, request, pk=None):
        crawler = Crawler()

        stdlogger.debug(pk)
        url = base64.b64decode(pk)
        stdlogger.info(url.decode())
        crawler.crawl_title(url.decode())
        serializer = serializers.CrawlSerializer(crawler)
        return Response(serializer.data)
