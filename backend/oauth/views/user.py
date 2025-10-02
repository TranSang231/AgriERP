import datetime
from uuid import UUID
from base.views import BaseViewSet
from common.constants import Http
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext as _
from base.utils import StringUtil
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from ..models import User
from ..serializers import UserSerializer


class UserViewSet(BaseViewSet):
    """
    :attr:alternate_required_scopes: dict keyed by method name with value: iterable alternate scope lists

    For each method (exp:retrieve, create, update ...), a list of lists of allowed scopes is tried in order and the first to match succeeds.

    @example
    required_alternate_scopes = {
       'create': [['user:create']],
       "activate": [["user:activate_user"]],
       'update': [['user:update','scope2'], ['alt-scope3'], ['alt-scope4','alt-scope5']] # one of all scope array which user scope had => permitted
    }
    Can define scope if you need, check in scopes.json file if scope doesn't exist please add it follow template
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    required_alternate_scopes = {
        "create": [["admin:users:edit"]],
        "invite": [["admin:users:edit"],],
        "retrieve": [
            ["admin:users:view"],
            ["admin:users:edit"],
        ],
        "update": [
            ["users:edit-mine"],
            ["admin:users:edit"],
        ],
        "destroy": [["admin:users:edit"]],
        "multiple_delele": [["admin:users:edit"]],
        "list": [["admin:users:view"], ["admin:users:edit"]],
        "change_password": [["users:edit-mine"]],
        "import_data": [["admin:users:edit"]],
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        params = request.query_params
        args = dict()
        
        active = params.get("active")
        if active:
            args.update(active=StringUtil.convert_to_int(active))
        
        keyword = params.get("keyword", None)
        if keyword:
            args.update(first_name__icontains=keyword)
            
        if args:
            queryset = queryset.filter(**args)

        if params.get('page_size') is not None:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)

    def multiple_delele(self, request, *args, **kwargs):
        ids = request.data.get("ids")
        manager = User.objects
        if ids:
            superuser_ids = manager.filter(is_superuser=True).values('id')
            exclude_ids = [item['id'].urn[9:] for item in superuser_ids]
            filtered_ids = [id for id in ids if not id in exclude_ids]
            if filtered_ids:
                with transaction.atomic():
                    instances = manager.filter(id__in=filtered_ids)
                    if instances:
                        instances.delete()
                self.clear_querysets_cache()
        return Response(filtered_ids)

    @action(methods=[Http.HTTP_PUT], detail=True)
    def change_password(self, request, *args, **kwargs):
        data = request.data
        user = self.get_object()
        password = data.get("old_password")
        password1 = data.get("new_password1")
        password2 = data.get("new_password2")
        if password1 and password2 and password1 != password2:
             return Response(
                {"message": _("The passwords are mismatch.")},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        try:
            password_validation.validate_password(password1,user)
        except ValidationError as error:
            return Response(
                {"message": _("The password is invalid format.")},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        
        try:
            user.set_password(password1)
            self.perform_update(user)
        except Exception as e:
            print(e)
            return Response(
                {"message": _("There is an error occur.")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
        return Response({"message": _("The password have been updated.")})
