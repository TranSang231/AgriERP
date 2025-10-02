from ..models import Bot
from rest_framework import serializers
from .intent_training import IntentTrainigSerializer
from .response import ResponseSerializer
from .entity import EntitySerializer
from .synonym import SynonymSerializer
from .story import StorySerializer
from .rule import RuleSerializer

class BotTrainingSerializer(serializers.ModelSerializer):
    intents = IntentTrainigSerializer(many=True, required=False)
    responses = ResponseSerializer(many=True, required=False)
    entities = EntitySerializer(many=True, required=False)
    synonyms = SynonymSerializer(many=True, required=False)
    stories = StorySerializer(many=True, required=False)
    rules = RuleSerializer(many=True, required=False)


    class Meta:
        model = Bot
        fields = [
            'id',
            'name',
            'config',
            'intents',
            'entities',
            'synonyms',
            'responses',
            'entities',
            'stories',
            'rules',
            'output_folder'
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            'name': {'required': False}
        }
