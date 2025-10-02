from .base import Const
from django.utils.translation import gettext as _

class Http(Const):
    # Methods
    HTTP_GET = "get"
    HTTP_POST = "post"
    HTTP_PUT = "put"
    HTTP_DELETE = "delete"
    HTTP_HEAD = "head"
    HTTP_OPTIONS = "options"
    HTTP_PATCH = "patch"
    HTTP_METHODS = (
        (HTTP_GET, _("GET")),
        (HTTP_POST, _("POST")),
        (HTTP_PUT, _("PUT")),
        (HTTP_DELETE, _("DELETE")),
        (HTTP_HEAD, _("HEAD")),
        (HTTP_OPTIONS, _("OPTIONS")),
        (HTTP_PATCH, _("PATCH")),
    )

    # Linitation options
    LIMIT_PER_HOUR = "hour"
    LIMIT_PER_DAY = "day"
    LIMIT_PER_WEEK = "week"
    LIMIT_PER_MONTH = "month"
    LIMIT_OPTIONS = (
        (LIMIT_PER_HOUR, _("Per Hour")),
        (LIMIT_PER_DAY, _("Per Day")),
        (LIMIT_PER_WEEK, _("Per week")),
        (LIMIT_PER_MONTH, _("Per month")),
    )
