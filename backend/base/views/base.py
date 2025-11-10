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
        # Support limit parameter (alias for page_size)
        limit = params.get('limit', None)
        if limit is not None:
            if page_size is None:  # Use limit as page_size if page_size not provided
                page_size = limit
            del params['limit']
        # Support ordering parameter
        ordering = params.get('ordering', None)
        if ordering is not None:
            del params['ordering']

        # Normalize aliases and handle category_id
        # If category_id exists, convert it for proper filtering
        if 'category_id' in params:
            category_id_value = params.get('category_id')
            # Only normalize if we have categories param already or if value is valid
            if category_id_value and category_id_value not in {"NaN", "nan", "undefined", "null", "None", "", "Null"}:
                params['categories'] = category_id_value
                del params['category_id']
        
        if 'category' in params and 'categories' not in params:
            params['categories'] = params.get('category')
            del params['category']

        # Remove invalid placeholder values
        invalid_values = {"NaN", "nan", "undefined", "null", "None", "", "Null"}

        query = None
        if keyword and len(self.search_map) > 0:
            query = Q()
            for field, op in self.search_map.items():
                try:
                    kwargs = {'{0}__{1}'.format(field, op): keyword}
                    query |= Q(**kwargs)
                except Exception:
                    # Field doesn't exist or invalid, skip it
                    continue

        for param, value in params.items():
            # Ignore empty or invalid values
            if value is None or (isinstance(value, str) and value.strip() in invalid_values):
                continue
            
            # Skip parameters that are purely numeric (likely malformed URL encoding)
            # or contain only special characters that aren't valid field names
            if param.isdigit() or not param.replace('_', '').replace('-', '').isalnum():
                continue
                
            try:
                if param[-2:] == '[]':
                    values = params.getlist(param)
                    # Filter out invalid values from the list
                    valid_values = [v for v in values if v not in invalid_values]
                    if not valid_values:
                        continue
                    kwargs = {'{0}__in'.format(param.rstrip('[]')): valid_values}
                else:
                    kwargs = {'{0}__exact'.format(param): value}
                
                # Try to build the query
                if query is None:
                    query = Q(**kwargs)
                else:
                    query = query & Q(**kwargs)
            except Exception:
                # Field doesn't exist or other error, skip this parameter
                continue

        # Wrap filter in try-except to handle FieldError gracefully
        if query is not None:
            try:
                queryset = queryset.filter(query)
            except Exception:
                # Field doesn't exist in model, return empty queryset or original queryset
                pass
                
        if ordering is not None and ordering != '':
            try:
                queryset = queryset.order_by(ordering)
            except Exception:
                # Invalid ordering, skip it
                pass
                
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
