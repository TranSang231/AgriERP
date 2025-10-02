from datetime import timedelta
from django.utils import timezone


class SectionFilterBackend():
    def filter_queryset(self, request, queryset, view):
        kwargs = view.kwargs
        site_id = kwargs.get('sites_pk', None)
        if site_id is not None:
            return queryset.filter(site__id=site_id)
        return queryset
