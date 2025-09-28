from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import pytz

utc=pytz.UTC

# Create your models here.
from oauth2_provider.models import (
    AbstractGrant,
    AbstractAccessToken,
    AbstractApplication,
    AbstractIDToken,
    AbstractRefreshToken
)


class Application(AbstractApplication):
    APPLICATION_TYPE_SYSTEM = "system"
    APPLICATION_TYPE_THIRD_PARTY = "third-party"
    APPLICATION_TYPE_CLIENT = "client"
    APPLICATION_TYPES = (
        (APPLICATION_TYPE_SYSTEM, _("The applications created by Alpha")),
        (APPLICATION_TYPE_THIRD_PARTY, _("The third-parties' applications")),
        (APPLICATION_TYPE_CLIENT, _("The application created by the businesses")),
    )
    scope = models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=APPLICATION_TYPES, default=APPLICATION_TYPE_CLIENT, blank=True)

class Grant(AbstractGrant):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

class IDToken(AbstractIDToken):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

class AccessToken(AbstractAccessToken):
    """
    Change token fields from char field to text field (fix token too long)
    """
    source_refresh_token = models.OneToOneField(
        # unique=True implied by the OneToOneField
        'oauth.RefreshToken',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="refreshed_access_token",
    )
    token = models.TextField(blank=True)
    token_checksum = models.CharField(max_length=64, blank=True, default='')
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    id_token = models.OneToOneField(
        IDToken,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="access_token",
    )

    def is_expired(self):
        """
        Check token expiration with timezone awareness
        """
        if not self.expires:
            return True

        return  timezone.now() >= utc.localize(self.expires)

class RefreshToken(AbstractRefreshToken):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="refresh_tokens")
    access_token = models.OneToOneField(
        AccessToken,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="refresh_token",
    )
