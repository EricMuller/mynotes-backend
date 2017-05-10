import django_filters
from rest_framework import filters
from apps.mywebmarks.models import Bookmark
from apps.mywebmarks.models import Folder
from apps.mywebmarks.models import Tag

from django.forms.fields import MultipleChoiceField
from django_filters.filters import MultipleChoiceFilter


class MultipleField(MultipleChoiceField):
    def valid_value(self, value):
        return True


class MultipleFilter(MultipleChoiceFilter):
    field_class = MultipleField


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class FolderFilter(filters.FilterSet):

    class Meta:
        model = Folder
        fields = ['id', 'tree_id', 'level', 'parent_id']


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
