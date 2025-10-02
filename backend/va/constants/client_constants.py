from . import NLUDataTypes, StoryStepTypes
from .nlu_config_template import nlu_config_template

client_constants = {
    "nlu_data_types": [{"value": x, "description": y} for x, y in NLUDataTypes.CHOICES],
    "story_step_types": [{"value": x, "description": y} for x, y in StoryStepTypes.CHOICES],
    "nlu_config_template": nlu_config_template
}