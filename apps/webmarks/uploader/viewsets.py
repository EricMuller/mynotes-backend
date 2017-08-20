from authentication.permissions import DefaultsAuthentificationMixin
from webmarks.bookmarks import models
from webmarks.bookmarks import serializers
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets


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
