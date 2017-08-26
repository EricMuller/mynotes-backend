from django.db.models import Q
# from django.db.models import F
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from apps.bookmarks.authentification import DefaultsAuthentificationMixin


class DefaultQueryFilter(object):
    OR = 'or__'
    AND = 'and__'
    IN = '__in'

    EXCLUDES = ('page', 'paginate_by')

    def create_filter_from_params(self, params, aqset=None):

        qset = Q()
        for param in params:
            name = param
            # value = param[1]
            values = params.get(param)
            if len(values) > 1 and name.find(self.IN) < 0:
                # name = name[:-len(self.IN)]
                for value in values:
                    qset = self.add_qset(qset, name, value)
            else:
                qset = self.add_qset(qset, name, values)

        return qset

    def create_filter_from_query_params(self, request, aqset=None):

        return self.create_filter_from_params(
            dict(request.query_params), aqset)

    def add_qset(self, qset, name, value):

        if name not in self.EXCLUDES:
            idx = name.find(self.OR)
            if idx is not None and idx == 0:
                name = name[len(self.OR):]
                qset |= Q(**{name: value})
            else:
                idx = name.find(self.AND)
                if idx is not None and idx == 0:
                    name = name[len(self.AND):]
                    qset &= Q(**{name: value})
                else:
                    qset &= Q(**{name: value})

        return qset


class QueryUserFilter(DefaultQueryFilter):

    def create_filter_from_query_params(self, request, **kwargs):
        return super(QueryUserFilter, self).create_filter_from_query_params(request, Q(user_cre=request.user))


class Filter(object):

    @staticmethod
    def create_filter_from_query_params(request):

        qset = Q(user_cre=request.user)
        params = request.query_params
        # import ipdb; ipdb.set_trace()
        for param in params:
            print(param)
        return qset


class QueryStandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, model, fields, data):

        return Response({
            'model': model,
            'fields': fields,
            'count': self.page.paginator.count,
            'next': self.get_next_number(),
            'current': self.page.number,
            'previous': self.get_previous_number(),
            'num_pages': (self.page.paginator.count // self.page_size),
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'page_size': self.page_size,
            'data': data,

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

# EverybodyCanAuthentication


class QueryModelViewSet(DefaultsAuthentificationMixin, viewsets.ModelViewSet):

    pagination_class = QueryStandardResultsSetPagination
    filter_class = QueryUserFilter
    # renderer_classes = (JSONRenderer, HTMLFormRenderer
    #    , BrowsableAPIRenderer )

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        queryset = self.queryset
        filters = self.filter_class().create_filter_from_query_params(self.request)
        # print(filters)
        if filters is not None:
            queryset = queryset.filter(filters)
        print(str(queryset.query))
        return queryset

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None

        serializer_class = self.get_serializer_class()
        model = self.queryset.model._meta.object_name
        fields = serializer_class.Meta.fields

        return self.paginator.get_paginated_response(model, fields, data)
