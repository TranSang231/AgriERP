import datetime

from base.views import BaseViewSet
from ..models import Holiday
from ..serializers import HolidaySerializer
from django.db.models import Q

class HolidayViewSet(BaseViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    required_alternate_scopes = {
        "create": [["offices:edit"]],
        "retrieve": [["offices:view"], ["offices:edit"]],
        "update": [["offices:edit"]],
        "destroy": [["offices:edit"]],
        "list": [["offices:view"], ["offices:edit"]]
    }

    def list(self, request, pk=None, *args, **kwargs):
        today = datetime.date.today()
        holidays = Holiday.objects.filter(
            Q(start_year__lte=today.year, end_year__gt=today.year, repeat=True)
            | Q(Q(start_date__year=today.year), Q(end_date__year=today.year)),
            office_id=kwargs["parent_lookup_e"],
        )
        page = self.paginate_queryset(holidays)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)
