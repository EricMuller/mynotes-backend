import django_filters
from django.forms.fields import MultipleChoiceField
from django_filters.filters import MultipleChoiceFilter


class MultipleField(MultipleChoiceField):
    def valid_value(self, value):
        return True


class MultipleFilter(MultipleChoiceFilter):
    field_class = MultipleField


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass
