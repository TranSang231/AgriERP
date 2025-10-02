from urllib.parse import urlparse
from ..models import Site


class DomainFilterBackend():
    def filter_queryset(self, request, queryset, view):
        origin = request.META.get("HTTP_ORIGIN")
        origin = (
            request.META.get("REMOTE_ADDR")
            if origin is None
            else origin
        )
        url = urlparse(origin)
        host = url.hostname
        host = (
            f"{host}:{url.port}"
            if url.port is not None and url.port != 80 and url.port != 443
            else host
        )
        if queryset is not None and queryset.model is not None:
            if queryset.model == Site:
                return queryset.filter(domain_name=host)
            if hasattr(queryset.model, 'site'):
                return queryset.filter(site__domain_name=host)
        return queryset
