import requests
from django.conf import settings

class Rasa:
    """
    Gateway  for Rasa
    """

    def __init__(self):
        self.endpoint = getattr(settings, 'RASA_ENDPOINT')

    def get_nlu_status(self):
        return requests.get(f"{self.endpoint}/status")
    
    def get_nlu_version(self):
        return requests.get(f"{self.endpoint}/version")
    
    def get_nlu_host(self):
        return getattr(settings, 'RASA_ENDPOINT')