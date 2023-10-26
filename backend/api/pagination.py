from rest_framework import pagination


class Pagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 6
    max_page_size = 6
