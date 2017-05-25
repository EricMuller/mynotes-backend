
from webmarks.storage import models
from webmarks.storage import serializers

from webmarks.drf_utils.viewsets import AggregateModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import renderers
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.http import HttpResponse


class ArchiveViewSet(AggregateModelViewSet):

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
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer

    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,
                        renderers.StaticHTMLRenderer,)

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
        """
            Download Archive File.
        """
        archive = get_object_or_404(models.Archive, pk=pk)
        # tmp = tempfile.NamedTemporaryFile(suffix=".note")
        filename = archive.name.split('/')[-1]
        resp = HttpResponse(
            archive.data, content_type='application/text;charset=UTF-8')
        resp['Content-Disposition'] = "attachment; filename=%s" % filename
        return resp
