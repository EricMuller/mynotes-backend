
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from rest_framework.utils.urls import remove_query_param


class NoPagination():

    def get_response(self, data):
        return Response({
            'count': data.count,
            'next': 1,
            'current': 1,
            'previous': 1,
            'num_pages': 1,
            'links': {
                'next': 1,
                'previous': 1
            },
            'data': data,
            'page_size': data.count

        })


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):

        return Response({
            'model': self.page.paginator.object_list.model._meta.object_name,
            'count': self.page.paginator.count,
            'next': self.get_next_number(),
            'current': self.page.number,
            'previous': self.get_previous_number(),
            'num_pages': (self.page.paginator.count // self.page_size),
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'data': data,
            'page_size': self.page_size,

        })

    def get_next_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_number(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()

        return page_number


class AggregateResultsViewSetPagination(PageNumberPagination):
    """
        ajout model et data aggregées
    """
    # page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, model, fields, data, aggregate_data):

        # import ipdb; ipdb.set_trace()
        model_name = model._meta.object_name
        page_size = self.get_page_size(self.request)
        count = self.page.paginator.count
        return Response({
            'model': model_name,
            'fields': fields,
            'count': count,
            'next': self.get_next_number(),
            'current': self.page.number,
            'previous': self.get_previous_number(),
            'num_pages': (count // page_size + 1),
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'page_size': page_size,
            'data': data,
            'aggregate_data': aggregate_data,

        })

    def get_next_link(self):
        if not self.page.has_next():
            return None
        # url = self.request.build_absolute_uri()
        url = self.request.path
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        #url = self.request.build_absolute_uri()
        url = self.request.path
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_next_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_number(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()

        return page_number


class LargeResultsSetPagination(StandardResultsSetPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
