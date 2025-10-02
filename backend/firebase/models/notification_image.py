from django.db import models
from base.models import TimeStampedModel

from django.conf import settings

class NotificationImage(TimeStampedModel):
    image = models.ImageField(upload_to='notification_images/')

    def get_image_url(self):
        # Returns the absolute URL for the image
        default_host = settings.DEFAULT_HOST
        default_scheme = (
            "http"
            if default_host.startswith("localhost") or default_host.startswith("127.0.0.1")
            else "https"
        )
        
        if settings.DEBUG:
            return f"{default_scheme}://{default_host}{self.image.url}"
        return f"{default_scheme}://{default_host}{self.image.url}"
    
    class Meta:
        db_table = "notification_images"