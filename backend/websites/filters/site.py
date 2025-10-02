from datetime import timedelta
from django.utils import timezone


class SiteFilterBackend():
    def filter_queryset(self, request, queryset, view):
        kwargs = view.kwargs
        site_id = kwargs.get('sites_pk', None)
        if site_id is None:
            site_id = kwargs.get('site_pk', None)
        if site_id is not None and queryset.model is not None:
            if hasattr(queryset.model, 'site'):
                return queryset.filter(site__id=site_id)
            elif hasattr(queryset.model, 'sites'):
                return queryset.filter(sites__id__in=[site_id])
        return queryset
