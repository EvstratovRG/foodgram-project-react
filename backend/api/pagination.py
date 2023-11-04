from rest_framework import pagination


class Pagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
