# from rest_auth.permissions import DefaultsAuthentificationMixin
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import permissions

from webmarks_crawler.crawler import Crawler
from . import serializers

import base64
import logging

stdlogger = logging.getLogger(__name__)


class CrawlerViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

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
