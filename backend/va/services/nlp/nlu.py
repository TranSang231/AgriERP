from .rasa import Rasa

class NLUService:
    client = Rasa()

    @classmethod
    def get_nlu_version(cls):
        return cls.client.get_nlu_version()
    
    @classmethod
    def get_nlu_status(cls):
        return cls.client.get_nlu_status()
    
    @classmethod
    def get_nlu_host(cls):
        return cls.client.get_nlu_host()