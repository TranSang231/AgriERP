import re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path
from django.views.static import serve


def static(prefix, view=serve, **kwargs):
    """
    Return a URL pattern for serving files in debug mode.

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        # ... the rest of your URLconf goes here ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    """
    if not prefix:
        raise ImproperlyConfigured("Empty static prefix not permitted")
    elif not settings.LOCAL_BUILD:
        # No-op if not in debug build or a non-local prefix.
        return []
    p = re.escape(prefix.lstrip("/"))
    return [
        re_path(
            r"^%s(?P<path>.*)$" % p, view, kwargs=kwargs
        ),
    ]
