from . import AccountStatus
from ..models import Application
client_constants = {
    "account_statuses": [{"value": x, "description": y} for x, y in AccountStatus.CHOICES],
    "application_types": [{"value": x, "description": y} for x, y in Application.APPLICATION_TYPES],
    "client_types": [{"value": x, "description": y} for x, y in Application.CLIENT_TYPES],
    "algorithm_types": [{"value": x, "description": y} for x, y in Application.ALGORITHM_TYPES],
    "grant_types": [{"value": x, "description": y} for x, y in Application.GRANT_TYPES]
}