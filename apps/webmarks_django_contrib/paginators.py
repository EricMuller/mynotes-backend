from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SpringSetPagination(PageNumberPagination):
    """
    Spring like pagination
    """

    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'content': data,
            'totalElements': self.page.paginator.count,
            'totalPages': (self.page.paginator.count // self.page_size) + 1,
            'last': 'false' if self.page.has_next() else 'true',
            'size': self.page_size,
            'number': self.page.number,
            'numberOfElements': len(data),
            'first': 'false' if self.page.has_previous() else 'true',
        })


class LargeResultsSetPagination(SpringSetPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
