from oauth.scopes import (
    scopes as oauth_scopes,
    default_scopes as oauth_default_scopes
)

from contents.scopes import (
    scopes as contents_scopes,
    default_scopes as contents_default_scopes
)

from businesses.scopes import (
    scopes as businesses_scopes,
    default_scopes as businesses_default_scopes
)
from hr.scopes import (
    scopes as hr_scopes,
    default_scopes as hr_default_scopes
)

from websites.scopes import (
    scopes as websites_scopes,
    default_scopes as websites_default_scopes
)

from va.scopes import (
    scopes as va_scopes,
    default_scopes as va_default_scopes
)

from knowledge.scopes import (
    scopes as knowledge_scopes,
    default_scopes as knowledge_default_scopes
)

from ecommerce.scopes import (
    scopes as ecommerce_scopes,
    default_scopes as ecommerce_default_scopes
)

scopes = {
    **oauth_scopes,
    **contents_scopes,
    **businesses_scopes,
    **hr_scopes,
    **websites_scopes,
    **va_scopes,
    **websites_scopes,
    **knowledge_scopes,
    **ecommerce_scopes
}

default_scopes = {
    **oauth_default_scopes,
    **contents_default_scopes,
    **websites_default_scopes,
    **hr_default_scopes,
    **businesses_default_scopes,
    **websites_default_scopes,
    **va_default_scopes,
    **knowledge_default_scopes,
    **ecommerce_default_scopes
}
