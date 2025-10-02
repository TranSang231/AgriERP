from django.db import models
from base.models import TimeStampedModel
from oauth.models import User


class UserToken(TimeStampedModel):
    user = models.ForeignKey(
        User, related_name="user_tokens", on_delete=models.CASCADE, blank=True)
    token = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.token}"

    class Meta:
        db_table = "user_tokens"
