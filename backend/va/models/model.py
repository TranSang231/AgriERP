from django.db import models
from base.models.timestamped import TimeStampedModel
from .bot import Bot
import os
def nlu_model_upload_path(instance, file_name):
    return os.path.join(instance.bot.output_folder,file_name)

class NLUModel(TimeStampedModel):
    name =  models.CharField(max_length=255, blank=True) 
    hash = models.CharField(max_length=64, blank=True, null=True)
    file = models.FileField(upload_to=nlu_model_upload_path)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.CASCADE, related_name="models")
    
    def __str__(self):
        return self.model_name
    
    class Meta:
        db_table = "va__nlu_models"