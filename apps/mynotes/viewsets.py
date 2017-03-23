import base64
import logging
from abc import ABCMeta, abstractmethod
from apps.mynotes import models
from apps.mynotes import serializers
from apps.mynotes.authentification import DefaultsAuthentificationMixin
from apps.mynotes.crawler import Crawler
from apps.mynotes.filters import NoteFilter
from apps.mynotes.managers import AggregateList
from apps.mynotes.paginators import AggregateResultsViewSetPagination

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


stdlogger = logging.getLogger(__name__)


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
    queryset = models.Note.objects.all()
    serializer_class = serializers.NoteSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    # filter_fields = ('id', 'title', 'public', 'description', )
    filter_class = NoteFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.NoteListSerializer

        return serializers.NoteSerializer


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


class CrawlerViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
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
        data = crawler.crawl_title(url.decode())
        serializer = serializers.CrawlSerializer(data)
        return Response(serializer.data)
