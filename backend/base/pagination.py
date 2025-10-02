from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "previous": self.get_previous_link(),
                    "next": self.get_next_link(),
                },
                "page": self.page.number,
                "page_size": self.get_page_size(self.request),
                "num_pages": self.page.paginator.num_pages,
                "count": self.page.paginator.count,
                "results": data,
            }
        )
