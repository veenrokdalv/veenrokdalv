from collections import OrderedDict

from rest_framework.pagination import CursorPagination as DRFCursorPagination
from rest_framework.response import Response


class CursorPagination(DRFCursorPagination):
    ordering = '-created_date'

    def get_count(self, queryset):
        """
        Определите количество объектов, поддерживающих либо наборы запросов, либо обычные списки.
        """
        try:
            return queryset.count()
        except (AttributeError, TypeError):
            return len(queryset)

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'nullable': False,
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                },
                'results': schema,
            },
        }

    def get_html_context(self):
        return {
            'count': self.count,
            'previous_url': self.get_previous_link(),
            'next_url': self.get_next_link()
        }