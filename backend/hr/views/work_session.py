from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from base.views import BaseViewSet
from common.utils import DataUtils
from common.constants import Http
from ..models import WorkSession
from ..serializers import WorkSessionSerializer


class WorkSessionViewSet(BaseViewSet):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    required_alternate_scopes = {
        "create": [["offices:edit"]],
        "retrieve": [["offices:view"], ["offices:edit"]],
        "update": [["offices:edit"]],
        "destroy": [["offices:edit"]],
        "create_multiple": [["offices:edit"]],
        "delete_by_day_of_week": [["offices:edit"]],
        "list": [["offices:view"], ["offices:edit"]],
    }

    @action(methods=[Http.HTTP_DELETE], detail=False)
    def delete_by_day_of_week(self, request, *args, **kwargs):
        day_of_week_param = DataUtils.cast_to_int(self.request.query_params.get("day_of_week", None), None)
        office_id = DataUtils.cast_to_int(
            self.request.query_params.get("office_id", None), None
        )
        if day_of_week_param is None:
            return Response(
                {"detail": "day_of_week param not found in url"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if office_id is None:
            return Response(
                {"detail": "office id param not found in url"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        WorkSession.objects.filter(day_of_week=day_of_week_param, office_id=office_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=[Http.HTTP_POST], detail=False)
    def create_multiple(self, request, *args, **kwargs):
        data = request.data
        work_day = data.get("work_day", None)
        office_id = data.get("office", None)
        sessions = data.get("sessions", [])

        if work_day is None:
            return Response(
                {"detail": "work_day field is empty"}, status=status.HTTP_400_BAD_REQUEST
            )
        if office_id is None:
            return Response(
                {"detail": "office_id field is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not sessions:
            return Response(
                {"detail": "sessions field is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for session in sessions:
            session["work_day"] = work_day
            session["office"] = office_id

        with transaction.atomic():
            serializer = self.get_serializer(data=sessions, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    def get_queryset(self):
        office_id = self.kwargs['office_pk']
        if office_id:
            return super().get_queryset().filter(office_id=office_id).order_by('work_day', 'start_time')
