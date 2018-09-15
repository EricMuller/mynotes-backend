from rest_framework import filters
from bookmarks.models import Note


class NoteFilter(filters.FilterSet):
    # min_price = django_filters.NumberFilter(name="price", lookup_expr='gte')
    # max_price = django_filters.NumberFilter(name="price", lookup_expr='lte')

    # tags = MultipleFilter(lookup_expr='in')

    class Meta:
        model = Note
        fields = ['id', 'title', 'public', 'description',
                  'kind', 'tags', 'updated_dt', 'status']
        ordering_fields = ('updated_dt')
        # ordering = ('username',)
        # order_by = ('updated_dt',)
