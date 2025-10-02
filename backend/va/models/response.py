from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot
# Create your models here.

def bot_response_image_path(instance, filename):
    return "\\".join(['bots',str(instance.bot_id),'images', str(instance.id), filename])
class Response(TimeStampedModel):
    name =  models.CharField(max_length=255, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=bot_response_image_path, max_length=255, blank=True, null=True)
    custom =  models.JSONField(null=True, blank=True)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.CASCADE, related_name="responses")
    def __str__(self):
        return self.text
    
    class Meta:
        db_table = "va_responses"