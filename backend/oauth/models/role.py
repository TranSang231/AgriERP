import uuid
from django.db import models
from django.utils import timezone


class Role(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )   
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.TextField(default="", null=True, blank=True)
    scope = models.TextField(default="", null=True, blank=True)
    last_modified_by = models.CharField(max_length=255, null=True, blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name
    
    @property
    def scopes(self):
        """
        Returns a dictionary of allowed scope names (as keys) with their descriptions (as values)
        """

        # Don't move this import to global scope, because it it lazay object.
        from oauth2_provider.scopes import get_scopes_backend
        all_scopes = get_scopes_backend().get_all_scopes()
        if self.scope == "__all__":
            return {name: desc for name, desc in all_scopes.items()}
        role_scopes = self.scope.split()
        return {name: desc for name, desc in all_scopes.items() if name in role_scopes}

    class Meta:
        db_table = "oauth_roles"
