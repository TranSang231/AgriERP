from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet
from common.constants import Http
from oauth.constants import AccountStatus
from businesses.models import Employee
from ..models import Namespace, Page
from ..serializers import GeneralStatisticSerializer, PagesCountByDateSerializer

User = get_user_model()

class StatisticViewSet(GenericViewSet):
    required_alternate_scopes = {
        "general": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]],
        "pages_created_by_date": [["knowledge:namespaces:view"], ["knowledge:namespaces:edit"]]
    }

    @action(detail=False, methods=[Http.HTTP_GET], url_path="general")
    def general(self, request, *args, **kwargs):
        """
        API to get general statistics
        Returns: total users, namespaces, and pages count
        """
        try:
            # Count total active users
            total_users = Employee.objects.filter(status=AccountStatus.ACTIVE).count()

            # Count total namespaces
            total_namespaces = Namespace.objects.count()

            # Count total pages
            total_pages = Page.objects.count()

            data = {
                'total_users': total_users,
                'total_namespaces': total_namespaces,
                'total_pages': total_pages,
                'time': timezone.now()
            }

            serializer = GeneralStatisticSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {'error': f'Failed to fetch general statistics.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=[Http.HTTP_GET], url_path="pages-created-by-date")
    def pages_created_by_date(self, request, *args, **kwargs):
        """
        API to get pages created, grouped by date
        Query parameters:
        - start_date: Start date (YYYY-MM-DD) - optional, defaults to 7 days ago
        - end_date: End date (YYYY-MM-DD) - optional, defaults to today
        """
        params = request.query_params
        start_date_str = params.get('start_date')
        end_date_str = params.get('end_date')
        end_date = (
            datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if end_date_str is not None
            else timezone.now().date()
        )
        start_date = (
            datetime.strptime(start_date_str, '%Y-%m-%d').date()
            if start_date_str is not None
            else end_date - timedelta(days=7)
        )
        if start_date > end_date:
            raise ValidationError(detail=_("Start date must be before or equal to end date."))
        
        if start_date > end_date:
            raise ValidationError(detail=_("'Date range cannot exceed 365 days."))
        try:
            # Query pages created within the date range
            pages_queryset = Page.objects.filter(
                    created_at__date__gte=start_date,
                    created_at__date__lte=end_date
                ).annotate(
                    created_date=TruncDate('created_at')
                ).values('created_date').annotate(
                    count=Count('id')
                ).order_by('created_date')

            # Format data
            pages_count_by_date = [
                {
                    'date': item['created_date'],
                    'count': item['count']
                }
                for item in pages_queryset
            ]

            serializer = PagesCountByDateSerializer(pages_count_by_date, many=True)
            return Response(
                {
                    'start_date': start_date,
                    'end_date': end_date,
                    'data': serializer.data
                }, 
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'error': f'Failed to fetch pages by date range: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )