# from webmarks.rest_auth.permissions import DefaultsAuthentificationMixin
from webmarks.bookmarks import models
from webmarks.bookmarks import serializers
from webmarks.drf_utils.cache import CustomListKeyConstructor
from webmarks.drf_utils.viewsets import AggregateModelViewSet

from rest_framework import filters
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework import permissions
import logging

stdlogger = logging.getLogger(__name__)


class NoteViewSet(AggregateModelViewSet):

    """
    retrieve:
        Return a Note instance.

    list:
        Return all Note instance , ordered by most recently created.

    create:
        Create a new Note.

    delete:
        Remove an existing Note.

    partial_update:
        Update one or more fields on an existing Note.

    update:
        Update a Note.
    """

    queryset = models.BookmarkSerializer.objects.prefetch_related('tags')
    serializer_class = serializers.BookmarkSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = BookmarkFilter
    permission_classes = (permissions.IsAuthenticated,)

    @cache_response(key_func=CustomListKeyConstructor())
    def list(self, *args, **kwargs):
        return super(NoteViewSet, self).list(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        # print('user_id=' + str(self.request.user.id))
        return models.Bookmark.objects.prefetch_related('tags').filter(
            user_cre_id=self.request.user.id)

    def get_serializer_class(self):
        # if self.action == 'list':
        #    return serializers.NoteListSerializer
        return serializers.BookmarkSerializer
