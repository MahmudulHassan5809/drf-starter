from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"

    def _get_next_page(self):
        if not self.page.has_next():
            return None
        page_number: int = self.page.next_page_number()
        return page_number

    def _get_previous_page(self):
        if not self.page.has_previous():
            return None
        page_number: int = self.page.previous_page_number()
        return page_number

    def get_page_size(self, request):
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size and page_size.isdigit():
            if request.query_params.get(self.page_size_query_param) == "0":
                return None
            elif request.query_params.get(self.page_size_query_param):
                return request.query_params.get(self.page_size_query_param)
        else:
            return self.page_size

    def get_paginated_response(self, data):
        return Response(
            {
                "meta_data": {
                    "total": self.page.paginator.count,
                    "page_size": self.get_page_size(self.request),
                    "next": self._get_next_page(),
                    "previous": self._get_previous_page(),
                },
                "data": data,
            }
        )


class Pagination:
    def __init__(self, total_pages, page, count, page_size):
        self._total_pages = total_pages
        self._page = page
        self._count = count
        self._page_size = page_size

    @property
    def _next(self):
        """
        Calculating the next page for pagination
        returns int() or None
        """
        if int(self._total_pages) - int(self._page) > 0:
            return self._page + 1
        return None

    @property
    def _previous(self):
        """
        Calculating the previous page for pagination
        returns int() or None
        """
        if int(self._total_pages) - int(self._page) >= 0 and int(self._page) - 1 > 0:
            return int(self._page) - 1
        return None

    def generate_pagination(self):
        """
        Generating the pagination data
        return dictionary object
        results (data) will be updated from the view
        """
        data = {
            "count": self._count,
            "page_size": self._page_size,
            "next": self._next,
            "previous": self._previous,
        }

        return data
