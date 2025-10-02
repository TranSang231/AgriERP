from django.db import transaction
from django.db.models import Q
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from .ai_search import AISearchViewSet


class ViewOnlyViewSet(AISearchViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    export_model = False


    def list(self, request, *args, **kwargs):
        queryset, page_size = self.processParams(request);
        if page_size is not None:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)

