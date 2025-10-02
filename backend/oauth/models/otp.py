import uuid
from django.db import models
from django.db.models import Manager
from django.utils import timezone


class OTPModel(models.Model):
    objects = Manager
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    payload = models.JSONField(null=True, blank=True)
    expires = models.DateTimeField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_expired(self):
        """
        Check token expiration with timezone awareness
        """
        if not self.expires:
            return True

        return timezone.now() >= self.expires

    class Meta:
        abstract = True
