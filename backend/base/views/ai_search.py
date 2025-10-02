from django.db import transaction
from django.db.models import Q
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_nested_forms.utils import NestedForm
from .base import BaseViewSet


class AISearchViewSet(GenericAPIView):
    queryset_map = {}
    search_map = {}
    serializer_class = None
    required_alternate_scopes = {}
    serializer_map = {}
    document_class = None

    def get_queryset(self):
        """
        Get action's queryset base on `queryset_map`
        :return: QuerySet
        """
        return self.queryset_map.get(self.action, self.queryset)

    def get_serializer_class(self):
        """
        Get action's serializer base on `serializer_map`
        :return: Serializer
        """
        return self.serializer_map.get(self.action, self.serializer_class)

    def processParams(self, request):
        kwargs = request.query_params.copy().dict()

        # Takeout specical params
        keyword = kwargs.get('keyword', None)
        ai_search = keyword is not None and not keyword.strip() == ''
        queryset = (
            self.filter_queryset(self.document_class.get_query_set(**kwargs))
            if ai_search
            else self.filter_queryset(self.get_queryset())
        )
        if keyword is not None:
            del kwargs['keyword']
        page_size =  kwargs.get('page_size', None)
        if page_size is not None:
            page_size = int(page_size)
            del kwargs['page_size']
        page =  kwargs.get('page', None)
        if page is not None:
            page = int(page)
            del kwargs['page']

        if not ai_search:
            query = None
            for param, value in kwargs.items():
                if param[-2:] == '[]':
                    kwargs = {'{0}__in'.format(param.rstrip('[]')): kwargs.getlist(param)}
                else:
                    kwargs = {'{0}__exact'.format(param): value}
                query = Q(**kwargs) if query is None else query & Q(**kwargs)
            if query is not None:
                queryset = queryset.filter(query)

        return queryset, page_size

