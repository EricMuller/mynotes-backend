import django_filters
from rest_framework import filters
from apps.mynotes.models import Note

from django.forms.fields import MultipleChoiceField
from django_filters.filters import MultipleChoiceFilter


class MultipleField(MultipleChoiceField):
    def valid_value(self, value):
        return True


class MultipleFilter(MultipleChoiceFilter):
    field_class = MultipleField


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class NoteFilter(filters.FilterSet):
    # min_price = django_filters.NumberFilter(name="price", lookup_expr='gte')
    # max_price = django_filters.NumberFilter(name="price", lookup_expr='lte')

    tags = MultipleFilter(lookup_expr='in')

    class Meta:
        model = Note
        fields = ['id', 'title', 'public', 'description',
                  'type', 'tags', 'updated_dt', 'status']
        ordering_fields = ('updated_dt')
        # ordering = ('username',)
        # order_by = ('updated_dt',)
