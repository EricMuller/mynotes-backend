from rest_framework import viewsets
from abc import ABCMeta
from .paginators import AggregateResultsViewSetPagination
from .managers import AggregateList


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class AggregatePaginationReponseMixin(object):

    pagination_class = AggregateResultsViewSetPagination

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None

        if isinstance(self.queryset, AggregateList):
            aggregate_data = self.queryset.aggregate_data
        else:
            aggregate_data = {}

        fields = self.serializer_class.Meta.fields
        return self.paginator.get_paginated_response(self.queryset.model,
                                                     fields,
                                                     data, aggregate_data)


class AggregateModelViewSet(AggregatePaginationReponseMixin,
                            viewsets.ModelViewSet):
    __metaclass__ = ABCMeta

    pass
