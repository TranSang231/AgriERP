from django.utils.translation import gettext as _
from common.constants import Language

nlu_config_template = [
    {
        'name': 'recipe',
        'label': _('Recipe'),
        'type': 'select',
        'default': 'default.v1',
        'options': [{'value': 'default.v1', 'label': 'default.v1'}]
    },
    {
        'name': 'language',
        'label': _('Language'),
        'type': 'select',
        'default': Language.EN,
        'options': [{"value": x, "label": y} for x, y in Language.CHOICES]
    },
    {
        'name': 'policies',
        'label': _('Policies'),
        'type': 'array',
        'itemOptions': [
            {
                'name': 'MemoizationPolicy',
                'label': 'MemoizationPolicy',
                'children': [
                    {
                        'name': 'name',
                        'label': _('Name'),
                        'type': 'label',
                        'default': 'MemoizationPolicy'
                    },
                    {
                        'name': 'max_history',
                        'label': _('Max history'),
                        'type': 'number',
                        'default': 10
                    }
                ]
            },
            {
                'name': 'TEDPolicy',
                'label': 'TEDPolicy',
                'children': [
                    {
                        'name': 'name',
                        'label': _('Name'),
                        'type': 'label',
                        'default': 'TEDPolicy'
                    },
                    {
                        'name': 'max_history',
                        'label': _('Max history'),
                        'type': 'number',
                        'default': 10
                    },
                    {
                        'name': 'epochs',
                        'label': _('Epochs'),
                        'type': 'number',
                        'default': 10
                    }
                ]
            },
            {
                'name': 'RulePolicy',
                'label': 'RulePolicy',
                'children': [
                    {
                        'name': 'name',
                        'label': _('Name'),
                        'type': 'label',
                        'default': 'RulePolicy'
                    },
                    {
                        'name': 'core_fallback_threshold',
                        'label': _('Core fallback threshold'),
                        'type': 'number',
                        'default': 0.3
                    },
                    {
                        'name': 'core_fallback_action_name',
                        'label': _('Core fallback action name'),
                        'type': 'text',
                        'default': 'action_default_fallback'
                    },
                    {
                        'name': 'enable_fallback_prediction',
                        'label': _('Enable fallback prediction'),
                        'type': 'bool',
                        'default': True
                    },
                    {
                        'name': 'check_for_contradictions',
                        'label': _('Check for contradictions'),
                        'type': 'bool',
                        'default': True
                    }
                ]
            }
        ]
    }
]