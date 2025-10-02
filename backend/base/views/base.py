from django.db import transaction
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_nested_forms.utils import NestedForm


class BaseViewSet(viewsets.ModelViewSet):
    queryset_map = {}
    search_map = {}
    serializer_class = None
    required_alternate_scopes = {}
    serializer_map = {}
    export_model = False

    def get_queryset(self):
        """
        Get action's queryset base on `queryset_map`
        :return: QuerySet
        """
        return self.queryset_map.get(self.action, self.queryset)

    def clear_querysets_cache(self):
        """
        Cleand the cache
        Use this in cacses you have update the data somewhere
        """
        if self.queryset is not None:
            self.queryset._result_cache = None

        for action, queryset in self.queryset_map.items():
            queryset._result_cache = None

    def get_serializer_class(self):
        """
        Get action's serializer base on `serializer_map`
        :return: Serializer
        """
        return self.serializer_map.get(self.action, self.serializer_class)

    def processParams(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        params = request.query_params.copy()

        # Takeout special params
        keyword = params.get('keyword', None)
        # Support both `keyword` and `search`
        if (keyword is None or keyword == '') and 'search' in params:
            keyword = params.get('search') or None
            del params['search']
        if keyword is not None:
            del params['keyword']

        page_size = params.get('page_size', None)
        if page_size is not None:
            del params['page_size']
        page = params.get('page', None)
        if page is not None:
            del params['page']
        # Support ordering parameter
        ordering = params.get('ordering', None)
        if ordering is not None:
            del params['ordering']

        # Normalize aliases
        if 'category' in params and 'categories' not in params:
            params['categories'] = params.get('category')
            del params['category']

        # Remove invalid placeholder values
        invalid_values = {"NaN", "nan", "undefined", "null", "None", ""}

        query = None
        if keyword and len(self.search_map) > 0:
            query = Q()
            for field, op in self.search_map.items():
                kwargs = {'{0}__{1}'.format(field, op): keyword}
                query |= Q(**kwargs)

        for param, value in params.items():
            # Ignore empty or invalid values
            if value is None or (isinstance(value, str) and value.strip() in invalid_values):
                continue
            if param[-2:] == '[]':
                values = params.getlist(param)
                if not values:
                    continue
                kwargs = {'{0}__in'.format(param.rstrip('[]')): values}
            else:
                kwargs = {'{0}__exact'.format(param): value}
            query = Q(**kwargs) if query is None else query & Q(**kwargs)

        if query is not None:
            queryset = queryset.filter(query)
        if ordering is not None and ordering != '':
            queryset = queryset.order_by(ordering)
        return queryset, page_size

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        content_type = request.content_type
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            self.clear_querysets_cache()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        content_type = request.content_type
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data
        serializer = self.get_serializer(self.get_object(), data=data)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            self.clear_querysets_cache()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset, page_size = self.processParams(request);
        if page_size is not None:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        self.clear_querysets_cache()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def multiple_delele(self, request, *args, **kwargs):
        """
        Delete multiple items.
        :return: Response
        """
        ids = request.data.get("ids")
        ModelClass = self.get_serializer_class().Meta.model
        manager = ModelClass._default_manager
        with transaction.atomic():
            instances = manager.filter(id__in=ids)
            if instances:
                instances.delete()
        self.clear_querysets_cache()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MultipleUpdateViewSet(BaseViewSet):
    def create(self, request, *args, **kwargs):
        """
        Create mutile items at once.
        :return: Response
        """
        data = request.data.copy()
        try:
            serializer = self.get_serializer(
                data=data, many=isinstance(data, list))
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                self.clear_querysets_cache()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def sync(self, request, *args, **kwargs):
        """
        Sync data from client to server. The item without id will be created.
        The item does not exist in client request will be removed.
        The others items will be updated.
        Only use this method for the small table where all data can be fit on one page.
        :return: Response
        """
        data = request.data.copy()
        try:
            queryset = self.get_queryset()
            if queryset:
                serializer = self.get_serializer(
                    queryset, data=data, many=isinstance(data, list), allow_null=True)
            else:
                serializer = self.get_serializer(
                    data=data, many=isinstance(data, list))
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                self.clear_querysets_cache()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise e
