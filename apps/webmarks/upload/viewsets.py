from webmarks.bookmarks import models
from webmarks.bookmarks import serializers
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets


class UploadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UploadSerializer
    parser_classes = (MultiPartParser, FormParser,)
    # overriding default query set
    queryset = models.Upload.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super(UploadViewSet, self).get_queryset(*args, **kwargs)
        qs = qs.filter(owner=self.request.user)
        return qs
