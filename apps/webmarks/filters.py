
import django_filters
from django.forms.fields import MultipleChoiceField
from django_filters.filters import MultipleChoiceFilter
from webmarks import models
from rest_framework import filters


class MultipleField(MultipleChoiceField):
    def valid_value(self, value):
        return True


class MultipleFilter(MultipleChoiceFilter):
    field_class = MultipleField


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class FolderFilter(filters.FilterSet):

    class Meta:
        model = models.Folder
        fields = ['id', 'tree_id', 'level', 'parent_id']
