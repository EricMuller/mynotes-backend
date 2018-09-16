import django_filters
from rest_framework import filters
from webmarks_django_contrib.filters import MultipleFilter
from webmarks_bookmarks.models import Bookmark
from webmarks_bookmarks.models import Tag


class TagFilter(django_filters.FilterSet):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'public']


class BookmarkFilter(filters.FilterSet):
    # min_price = django_filters.NumberFilter(name="price", lookup_expr='gte')
    # max_price = django_filters.NumberFilter(name="price", lookup_expr='lte')

    tags = MultipleFilter(lookup_expr='in')

    class Meta:
        model = Bookmark
        fields = ['id', 'title', 'public', 'description',
                  'kind', 'tags', 'updated_dt', 'status']
        ordering_fields = ('updated_dt')
        # ordering = ('username',)
        # order_by = ('updated_dt',)
