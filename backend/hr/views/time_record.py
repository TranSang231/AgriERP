from django.utils import timezone
from rest_framework import decorators, status
from rest_framework.response import Response

from base.views import BaseViewSet
from hr.models.time_record import TimeRecord
from hr.serializers.time_record import TimeRecordSerializer


class TimeRecordViewSet(BaseViewSet):
    queryset = TimeRecord.objects.all().order_by('-check_in_at')
    serializer_class = TimeRecordSerializer
    search_map = {
        'note': 'icontains',
        'source': 'icontains',
    }

    @decorators.action(methods=['post'], detail=False, url_path='check-in')
    def check_in(self, request):
        data = request.data.copy()
        if 'check_in_at' not in data:
            data['check_in_at'] = timezone.now()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)

    @decorators.action(methods=['post'], detail=True, url_path='check-out')
    def check_out(self, request, pk=None):
        try:
            record = self.get_queryset().get(pk=pk)
        except TimeRecord.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        check_out_at = request.data.get('check_out_at') or timezone.now()
        record.close(check_out_at=check_out_at)
        record.save(update_fields=['check_out_at', 'duration_seconds', 'modified'])
        return Response(self.get_serializer(record).data, status=status.HTTP_200_OK)



