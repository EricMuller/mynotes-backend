# from rest_auth.permissions import DefaultsAuthentificationMixin
import logging

from rest_framework import filters
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.cache.decorators import cache_response

from webmarks_bookmarks.models import Bookmark
from webmarks_bookmarks.serializers import BookmarkSerializer
from webmarks_django_contrib.cache import CustomListKeyConstructor
from webmarks_django_contrib.paginators import SpringSetPagination

stdlogger = logging.getLogger(__name__)


class NoteViewSet(ModelViewSet):

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

    queryset = BookmarkSerializer.objects.prefetch_related('tags')
    serializer_class = BookmarkSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = SpringSetPagination

    @cache_response(key_func=CustomListKeyConstructor())
    def list(self, *args, **kwargs):
        return super(NoteViewSet, self).list(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        # print('user_id=' + str(self.request.user.id))
        return Bookmark.objects.prefetch_related('tags').filter(
            user_cre_id=self.request.user.id)

    def get_serializer_class(self):
        # if self.action == 'list':
        #    return serializers.NoteListSerializer
        return BookmarkSerializer
