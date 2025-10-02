from django.db import models
from .oauth2 import Application
from ..managers import ApiKeyManager

from oauthlib.oauth2.rfc6749.utils import scope_to_list
from rest_framework_api_key.models import AbstractAPIKey

class ApiKey(AbstractAPIKey):
    objects = ApiKeyManager()
    scope = models.TextField(blank=True)
    application = models.ForeignKey(
        Application,
        null=True,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    def has_scopes(self, scopes: str) -> bool:
        if self.scope == "__all__":
            return True
        else:
            key_scopes = set(scope_to_list(self.scope))
            view_scopes = set(scopes)
            return view_scopes.issubset(key_scopes)
