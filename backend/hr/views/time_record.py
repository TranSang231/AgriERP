from django.utils import timezone
from django.db.models import Q
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
    required_alternate_scopes = {
        'list': ['timekeeping:view'],
        'retrieve': ['timekeeping:view'],
        'create': ['timekeeping:edit'],
        'update': ['timekeeping:edit'],
        'destroy': ['timekeeping:manage'],
        'check_in': ['timekeeping:check'],
        'check_out': ['timekeeping:check'],
        'current_session': ['timekeeping:view'],
        'daily_summary': ['timekeeping:view'],
    }

    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = super().get_queryset()
        
        # Filter by employee
        employee_id = self.request.query_params.get('employee_id')
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
            
        # Filter by office
        office_id = self.request.query_params.get('office_id')
        if office_id:
            queryset = queryset.filter(office_id=office_id)
            
        # Filter by date range
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(check_in_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(check_in_at__date__lte=date_to)
            
        return queryset

    @decorators.action(methods=['post'], detail=False, url_path='check-in')
    def check_in(self, request):
        data = request.data.copy()
        employee_id = data.get('employee_id')
        
        if not employee_id:
            return Response(
                {'employee_id': ['This field is required.']}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if employee has an open session
        open_session = TimeRecord.objects.filter(
            employee_id=employee_id,
            check_out_at__isnull=True
        ).first()
        
        if open_session:
            return Response(
                {'detail': 'Employee already has an open session. Please check out first.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
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

        if record.check_out_at:
            return Response(
                {'detail': 'Session already closed.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        check_out_at = request.data.get('check_out_at') or timezone.now()
        record.close(check_out_at=check_out_at)
        record.save(update_fields=['check_out_at', 'duration_seconds', 'modified'])
        return Response(self.get_serializer(record).data, status=status.HTTP_200_OK)

    @decorators.action(methods=['get'], detail=False, url_path='current-session')
    def current_session(self, request):
        """Get current open session for an employee"""
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response(
                {'employee_id': ['This field is required.']}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            current = TimeRecord.objects.get(
                employee_id=employee_id,
                check_out_at__isnull=True
            )
            return Response(self.get_serializer(current).data, status=status.HTTP_200_OK)
        except TimeRecord.DoesNotExist:
            return Response({'detail': 'No open session found.'}, status=status.HTTP_404_NOT_FOUND)

    @decorators.action(methods=['get'], detail=False, url_path='daily-summary')
    def daily_summary(self, request):
        """Get daily summary for an employee"""
        employee_id = request.query_params.get('employee_id')
        date = request.query_params.get('date', timezone.now().date())
        
        if not employee_id:
            return Response(
                {'employee_id': ['This field is required.']}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        records = TimeRecord.objects.filter(
            employee_id=employee_id,
            check_in_at__date=date
        ).order_by('check_in_at')
        
        total_duration = sum(
            record.duration_seconds or 0 
            for record in records 
            if record.check_out_at
        )
        
        open_sessions = records.filter(check_out_at__isnull=True).count()
        
        return Response({
            'date': date,
            'employee_id': employee_id,
            'total_records': records.count(),
            'total_duration_seconds': total_duration,
            'total_duration_hours': round(total_duration / 3600, 2),
            'open_sessions': open_sessions,
            'records': self.get_serializer(records, many=True).data
        }, status=status.HTTP_200_OK)



