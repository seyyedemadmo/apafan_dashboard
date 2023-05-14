from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        temp = self.request
        return Response({
            'results': {
                'count': self.page.paginator.count,
                'next_page': self.get_next_link(),
                'previous_page': self.get_previous_link(),
                'results': data
            },
            'success': True,
            'message': 'Pagination successful.',
            'status': 200,
        })