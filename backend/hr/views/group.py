from ast import keyword
from base.views import BaseViewSet
from ..models import Group
from ..serializers import GroupSerializer, GroupTreeSerializer
from common.constants import Http
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class GroupViewSet(BaseViewSet):
    queryset = Group.objects.all()
    queryset_map = {
        "retrieve": Group.objects.select_related("manager")
            .prefetch_related("offices"),
    }
    serializer_class = GroupSerializer
    serializer_map = {
        "tree": GroupTreeSerializer,
    }
    required_alternate_scopes = {
        "create": [["offices:edit"]],
        "retrieve": [["offices:view"], ["offices:edit"]],
        "update": [["offices:edit"]],
        "destroy": [["offices:edit"]],
        "list": [["offices:view"], ["offices:edit"]],
        "tree": [["offices:view"], ["offices:edit"]],
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        params = request.query_params

        keyword = params.get("keyword", None)
        if keyword:
            queryset = queryset.filter(name__contains=keyword)
        
        if params.get('page_size') is not None:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)

    @action(methods=[Http.HTTP_GET], detail=False)
    def tree(self, request, *args, **kwargs):
        query_set = self.get_queryset().filter(parent=None)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
