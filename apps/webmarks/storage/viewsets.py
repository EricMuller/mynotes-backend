from webmarks.authentication.permissions import DefaultsAuthentificationMixin
from webmarks.bookmarks import models
from webmarks.bookmarks import serializers
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets



class FileStorageViewSet(DefaultsAuthentificationMixin,
                          viewsets.ModelViewSet):
  
    parser_classes = (FileUploadParser)
    # overriding default query set
  

    